from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from .database.db import *
from typing import List
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI()

class Reservations(BaseModel):
    reservation_id: str
    user_email: str
    book_id: str
    reservation_date: datetime
    expiration_date: datetime
    status: str
    user_id: str

