from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from infrastructure.databases.database import init_db, db
from infrastructure.models.watch_model import WatchModel
from infrastructure.models.seller_model import SellerModel
from domain.price_suggestion import suggest_price
import datetime

app = Flask(__name__)
CORS(app)
init_db(app)

api = Api(app, title='Watch Appraisers API', version='1.0', description='API for watch appraisal system')

appraisal_model = api.model('Appraisal', {
    'appraisedValue': fields.Float(required=True),
    'condition': fields.String(required=True),
    'notes': fields.String()
})

@api.route('/watches/pending')
class PendingWatches(Resource):
    def get(self):
        watches = WatchModel.query.filter_by(appraisal_status='pending').all()
        return [{'id': w.id, 'model': w.model, 'brand': w.brand, 'year': w.year, 'condition': w.condition, 'appraisal_status': w.appraisal_status} for w in watches]

@api.route('/appraisals/<int:watch_id>')
class AppraisalResource(Resource):
    @api.expect(appraisal_model)
    def post(self, watch_id):
        watch = WatchModel.query.get(watch_id)
        if not watch:
            return {'error': 'Watch not found'}, 404
        data = request.get_json()
        watch.appraisal_status = 'completed'
        db.session.commit()
        return {'id': watch.id, **data, 'appraiserId': 'testUserId', 'createdAt': str(datetime.datetime.now())}

    @api.expect(appraisal_model)
    def put(self, watch_id):
        watch = WatchModel.query.get(watch_id)
        if not watch:
            return {'error': 'Watch not found'}, 404
        data = request.get_json()
        for key, value in data.items():
            setattr(watch, key, value)
        watch.updated_at = datetime.datetime.now()
        db.session.commit()
        return {'id': watch.id, **data}

@api.route('/watches/<int:id>/suggest-price')
class SuggestPrice(Resource):
    def get(self, id):
        watch = WatchModel.query.get(id)
        if not watch:
            return {'error': 'Watch not found'}, 404
        return {'suggestedPrice': suggest_price(watch)}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)