import pytest
from httpx import AsyncClient
from main import app
from pymongo import MongoClient
from bson import ObjectId
import os

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def mongo_db():
    client = MongoClient(os.getenv("MONGO_URI_TEST", "mongodb://localhost:27017"))
    db = client["test_watch_appraisal"]
    yield db
    client.drop_database("test_watch_appraisal")
    client.close()

@pytest.fixture
async def token():
    return "mock_jwt_token"  # Mock JWT token

@pytest.mark.asyncio
async def test_create_appraisal(client, mongo_db, token):
    # Setup: Create a mock watch
    watch_data = {
        "brand": "Rolex",
        "model": "Submariner",
        "year": 2020,
        "condition": "good",
        "appraisalStatus": "pending"
    }
    watch_id = str(mongo_db.watches.insert_one(watch_data).inserted_id)

    # Test successful creation
    response = await client.post(
        f"/appraisals/{watch_id}",
        json={
            "appraisedValue": 5000,
            "condition": "good",
            "notes": "Minor scratches on bezel"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    assert response.json()["appraisedValue"] == 5000
    assert response.json()["condition"] == "good"
    assert response.json()["notes"] == "Minor scratches on bezel"

    # Verify watch status updated
    watch = mongo_db.watches.find_one({"_id": ObjectId(watch_id)})
    assert watch["appraisalStatus"] == "completed"

@pytest.mark.asyncio
async def test_create_appraisal_watch_not_found(client, token):
    # Test when watch does not exist
    response = await client.post(
        "/appraisals/123456789012345678901234",
        json={
            "appraisedValue": 5000,
            "condition": "good",
            "notes": "Minor scratches"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Watch not found"