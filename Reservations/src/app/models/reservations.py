from fastapi import FastAPI
from pydantic import BaseModel
from .database.db import *
from typing import List
from datetime import datetime
from bson import ObjectId
from pydantic import field_validator

app = FastAPI()

class Reservations(BaseModel):
    reservation_id: str
    user_email: str
    book_id: str
    reservation_date: str
    expiration_date: str
    status: str
    user_id: str
    isbn: str
    
    @field_validator('reservation_id', 'user_id', mode='before')
    def convert_objectid(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @field_validator('reservation_date', 'expiration_date', mode='before')
    def convert_datetime(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v

    class Config:
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}

@app.get("/holds/", response_model=List[Reservations])
def list_holds():
    db = get_db()
    holds = list(db["reservations"].find())
    for hold in holds:
        hold["_id"] = str(hold["_id"])  # Convert MongoDB ObjectId to string
        hold["reservation_id"] = str(hold["reservation_id"]) if isinstance(hold["reservation_id"], ObjectId) else hold["reservation_id"]
        hold["user_id"] = str(hold["user_id"]) if isinstance(hold["user_id"], ObjectId) else hold["user_id"]
    return [Reservations(**hold) for hold in holds]
