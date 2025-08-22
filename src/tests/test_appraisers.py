import pytest
from app import app
from infrastructure.models.watch_model import WatchModel, SupportTicket, Feedback
from infrastructure.databases.database import db

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            # Thêm dữ liệu mẫu
            watch = WatchModel(model="Submariner", brand="Rolex", year=2020, condition="good", appraisal_status="pending", seller_id=1)
            ticket = SupportTicket(customer_id=1, title="Issue with appraisal", description="Need help", status="open")
            db.session.add_all([watch, ticket])
            db.session.commit()
        yield client

def test_get_pending_watches(client):
    response = client.get('/watches/pending')
    assert response.status_code == 200
    assert len(response.get_json()) > 0

def test_get_support_tickets(client):
    response = client.get('/api/support/tickets?page=1&per_page=10')
    assert response.status_code == 200
    data = response.get_json()
    assert 'tickets' in data
    assert 'total' in data

def test_resolve_ticket(client):
    ticket = SupportTicket.query.filter_by(status='open').first()
    response = client.put(f'/api/support/tickets/{ticket.id}/resolve')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Ticket resolved'
    updated_ticket = SupportTicket.query.get(ticket.id)
    assert updated_ticket.status == 'resolved'

def test_submit_feedback(client):
    ticket = SupportTicket.query.filter_by(status='open').first()
    response = client.post('/api/support/feedback', json={
        'ticket_id': ticket.id,
        'customer_id': 1,
        'rating': 4,
        'comment': 'Good support'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert 'feedback_id' in data