from fastapi import FastAPI
from pydantic import BaseModel
from .database.db import *
from typing import List
from datetime import datetime
from bson import ObjectId
from pydantic import field_validator
from fastapi.responses import JSONResponse

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

