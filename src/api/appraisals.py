from fastapi import APIRouter, HTTPException, Depends, status
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from typing import List
from infrastructure.models.models import Watch, Appraisal, AppraisalInput
from domain.price_suggestion import suggest_price
import os
from config import config

router = APIRouter()

# MongoDB connection
client = MongoClient(config.MONGO_URI)
db = client["watch_appraisal"]
watches_collection = db["watches"]
appraisals_collection = db["appraisals"]

async def get_current_user(token: str = Depends(oauth2_scheme)):
    return {"user_id": "testUserId"}  # Mock user

# GET /api/watches/pending
@router.get("/watches/pending", response_model=List[Watch])
async def get_pending_watches(current_user: dict = Depends(get_current_user)):
    try:
        watches = watches_collection.find({"appraisalStatus": "pending"})
        return [Watch(id=str(watch["_id"]), **watch) for watch in watches]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error")

# POST /api/appraisals/{watchId}
@router.post("/appraisals/{watchId}", response_model=Appraisal, status_code=status.HTTP_201_CREATED)
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
@router.put("/appraisals/{id}", response_model=Appraisal)
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
@router.get("/watches/{id}/suggest-price")
async def suggest_price_endpoint(id: str, current_user: dict = Depends(get_current_user)):
    try:
        watch = watches_collection.find_one({"_id": ObjectId(id)})
        if not watch:
            raise HTTPException(status_code=404, detail="Watch not found")

        suggested_price = suggest_price(watch)
        return {"suggestedPrice": suggested_price}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error")