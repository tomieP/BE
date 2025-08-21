from flask_restx import Namespace, Resource, fields
from infrastructure.models.watch_model import Watch
from domain.price_suggestion import suggest_price
from flask import request

api = Namespace('appraisals', description='Watch appraisal operations')

appraisal_model = api.model('Appraisal', {
    'appraisedValue': fields.Float(required=True),
    'condition': fields.String(required=True),
    'notes': fields.String()
})

@api.route('/watches/pending')
class PendingWatches(Resource):
    def get(self):
        watches = Watch.query.filter_by(appraisal_status='pending').all()
        return [{'id': w.id, 'brand': w.brand, 'model': w.model, 'year': w.year, 'condition': w.condition, 'appraisal_status': w.appraisal_status} for w in watches]

@api.route('/appraisals/<int:watch_id>')
class AppraisalResource(Resource):
    @api.expect(appraisal_model)
    def post(self, watch_id):
        watch = Watch.query.get_or_404(watch_id)
        data = request.get_json()
        watch.appraisal_status = 'completed'
        # Giả lập lưu appraisal (thêm bảng appraisal nếu cần)
        return {'id': watch.id, **data, 'appraiserId': 'testUserId', 'createdAt': str(datetime.now())}

    @api.expect(appraisal_model)
    def put(self, watch_id):
        watch = Watch.query.get_or_404(watch_id)
        data = request.get_json()
        # Giả lập cập nhật
        return {'id': watch.id, **data}

@api.route('/watches/<int:id>/suggest-price')
class SuggestPrice(Resource):
    def get(self, id):
        watch = Watch.query.get_or_404(id)
        return {'suggestedPrice': suggest_price({'brand': watch.brand, 'model': watch.model, 'condition': watch.condition})}