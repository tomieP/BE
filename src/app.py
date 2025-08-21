# app/main.py
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer
import os

app = FastAPI(title="Watch Appraisers API")

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client["watch_appraisal"]
watches_collection = db["watches"]
appraisals_collection = db["appraisals"]

# Mock authentication (giả định JWT)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    return {"user_id": "testUserId"}  # Mock user

# Pydantic models
class Watch(BaseModel):
    id: str
    brand: str
    model: str
    year: int
    condition: str
    appraisalStatus: str

    class Config:
        json_encoders = {ObjectId: str}

class AppraisalInput(BaseModel):
    appraisedValue: float
    condition: str
    notes: Optional[str] = None

class Appraisal(BaseModel):
    id: str
    watchId: str
    appraisedValue: float
    condition: str
    notes: Optional[str] = None
    appraiserId: str
    createdAt: str

    class Config:
        json_encoders = {ObjectId: str}

# GET /api/watches/pending
@app.get("/api/watches/pending", response_model=List[Watch])
async def get_pending_watches(current_user: dict = Depends(get_current_user)):
    try:
        watches = watches_collection.find({"appraisalStatus": "pending"})
        return [Watch(id=str(watch["_id"]), **watch) for watch in watches]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error")

# POST /api/appraisals/{watchId}
@app.post("/api/appraisals/{watchId}", response_model=Appraisal, status_code=status.HTTP_201_CREATED)
async def create_appraisal(watchId: str, appraisal: AppraisalInput, current_user: dict = Depends(get_current_user)):
    try:
        watch = watches_collection.find_one({"_id": ObjectId(watchId)})
        if not watch:
            raise HTTPException(status_code=404, detail="Watch not found")

        appraisal_data = {
            "watchId": watchId,
            "appraisedValue": appraisal.appraisedValue,
            "condition": appraisal.condition,
            "notes": appraisal.notes,
            "appraiserId": current_user["user_id"],
            "createdAt": str(datetime.now())
        }
        result = appraisals_collection.insert_one(appraisal_data)
        watches_collection.update_one(
            {"_id": ObjectId(watchId)},
            {"$set": {"appraisalStatus": "completed"}}
        )
        appraisal_data["id"] = str(result.inserted_id)
        return Appraisal(**appraisal_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error")

# PUT /api/appraisals/{id}
@app.put("/api/appraisals/{id}", response_model=Appraisal)
async def update_appraisal(id: str, appraisal: AppraisalInput, current_user: dict = Depends(get_current_user)):
    try:
        existing_appraisal = appraisals_collection.find_one({"_id": ObjectId(id)})
        if not existing_appraisal:
            raise HTTPException(status_code=404, detail="Appraisal not found")

        update_data = {
            "appraisedValue": appraisal.appraisedValue,
            "condition": appraisal.condition,
            "notes": appraisal.notes
        }
        appraisals_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {k: v for k, v in update_data.items() if v is not None}}
        )
        updated_appraisal = appraisals_collection.find_one({"_id": ObjectId(id)})
        updated_appraisal["id"] = str(updated_appraisal["_id"])
        return Appraisal(**updated_appraisal)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error")

# GET /api/watches/{id}/suggest-price
@app.get("/api/watches/{id}/suggest-price")
async def suggest_price(id: str, current_user: dict = Depends(get_current_user)):
    try:
        watch = watches_collection.find_one({"_id": ObjectId(id)})
        if not watch:
            raise HTTPException(status_code=404, detail="Watch not found")

        # Mock market data
        mock_market_data = {
            "similarWatches": [
                {"brand": watch["brand"], "model": watch["model"], "price": 5000, "condition": "excellent"},
                {"brand": watch["brand"], "model": watch["model"], "price": 4500, "condition": "good"},
                {"brand": watch["brand"], "model": watch["model"], "price": 4000, "condition": "fair"}
            ]
        }

        average_price = sum(item["price"] for item in mock_market_data["similarWatches"]) / len(mock_market_data["similarWatches"])
        condition_multiplier = {"excellent": 1.2, "good": 1.0, "fair": 0.8}.get(watch["condition"], 1.0)
        suggested_price = average_price * condition_multiplier

        return {"suggestedPrice": suggested_price}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error")