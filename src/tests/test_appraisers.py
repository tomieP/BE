import pytest
from app import app
from infrastructure.models.watch_model import WatchModel
from infrastructure.databases.database import db

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()  # Xóa bảng test
            db.create_all()
            watch = WatchModel(model="Submariner", brand="Rolex", year=2020, condition="good", appraisal_status="pending", seller_id=1)
            db.session.add(watch)
            db.session.commit()
        yield client

def test_get_pending_watches(client):
    response = client.get('/watches/pending')
    assert response.status_code == 200
    assert len(response.json) > 0