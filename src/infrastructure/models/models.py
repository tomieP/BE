from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime
from typing import Optional

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