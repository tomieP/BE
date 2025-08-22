from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource, fields, reqparse
from infrastructure.databases.database import init_db, db
from infrastructure.models.watch_model import WatchModel, SellerModel, SupportTicket, Feedback
from domain.price_suggestion import suggest_price
import datetime

app = Flask(__name__)
CORS(app)
init_db(app)

api = Api(app, title='Watch Appraisers and Support API', version='1.0', description='API for watch appraisal and customer support system')

# Swagger models
appraisal_model = api.model('Appraisal', {
    'appraisedValue': fields.Float(required=True),
    'condition': fields.String(required=True),
    'notes': fields.String()
})

ticket_model = api.model('SupportTicket', {
    'customer_id': fields.Integer(required=True),
    'title': fields.String(required=True),
    'description': fields.String(),
    'status': fields.String(),
    'assigned_to': fields.Integer()
})

feedback_model = api.model('Feedback', {
    'ticket_id': fields.Integer(),
    'customer_id': fields.Integer(required=True),
    'rating': fields.Integer(required=True, description='1-5'),
    'comment': fields.String()
})

# Parser for GET /api/support/tickets
ticket_parser = reqparse.RequestParser()
ticket_parser.add_argument('page', type=int, default=1, help='Page number')
ticket_parser.add_argument('per_page', type=int, default=10, help='Items per page')
ticket_parser.add_argument('status', type=str, help='Filter by status (e.g., open, resolved)')

# Watch Endpoints
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

# Support Endpoints
@api.route('/api/support/tickets')
class SupportTickets(Resource):
    @api.doc(parser=ticket_parser)
    def get(self):
        args = ticket_parser.parse_args()
        page = args['page']
        per_page = args['per_page']
        status = args['status']

        query = SupportTicket.query
        if status:
            query = query.filter_by(status=status)
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        tickets = [{
            'id': t.id,
            'customer_id': t.customer_id,
            'title': t.title,
            'description': t.description,
            'status': t.status,
            'assigned_to': t.assigned_to,
            'created_at': t.created_at.isoformat(),
            'updated_at': t.updated_at.isoformat()
        } for t in pagination.items]
        return {
            'tickets': tickets,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }

@api.route('/api/support/tickets/<int:id>/resolve')
class ResolveTicket(Resource):
    def put(self, id):
        ticket = SupportTicket.query.get_or_404(id)
        if ticket.status == 'resolved':
            return {'message': 'Ticket already resolved'}, 400
        ticket.status = 'resolved'
        ticket.assigned_to = 1  # Giả sử assign cho nhân viên ID 1
        ticket.updated_at = datetime.datetime.now()
        db.session.commit()
        return {'message': 'Ticket resolved', 'ticket_id': id}

@api.route('/api/support/feedback')
class FeedbackResource(Resource):
    @api.expect(feedback_model)
    def post(self):
        data = request.get_json()
        new_feedback = Feedback(
            ticket_id=data.get('ticket_id'),
            customer_id=data['customer_id'],
            rating=data['rating'],
            comment=data.get('comment')
        )
        db.session.add(new_feedback)
        db.session.commit()
        return {'message': 'Feedback submitted', 'feedback_id': new_feedback.id}, 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)