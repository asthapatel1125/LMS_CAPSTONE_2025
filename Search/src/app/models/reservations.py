from datetime import datetime, timedelta
import uuid
from bson import ObjectId
from fastapi import FastAPI, APIRouter, HTTPException, Request
import jwt
from pydantic import BaseModel, Field, HttpUrl, field_validator
from controllers.token import SECRET_KEY
from .database.db import *
from typing import List
from pymongo import DESCENDING

app = FastAPI()
db = get_db()


class Book(BaseModel):
    title: str
    author: str
    genre: str
    rating: float
    kidFriendly: bool
    description: str
    format: str
    pageNumber: int
    publisher: str
    status: str
    isbn: str
    numOfMins: int
    numCopies: int
    
    
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
        
        
        
def normalize_bson(book: dict) -> dict:
    if "_id" in book:
        del book["_id"]

    fields = ["pageNumber", "numCopies", "numOfMins"]
    for field in fields:
        if isinstance(book.get(field), dict) and "$numberInt" in book[field]:
            book[field] = int(book[field]["$numberInt"])
        else:
            book[field] = int(book.get(field, 0))  # Default to 0 if missing

    if isinstance(book.get("kidFriendly"), dict) and "$numberInt" in book["kidFriendly"]:
        book["kidFriendly"] = bool(book["kidFriendly"]["$numberInt"])
    else:
        book["kidFriendly"] = book.get("kidFriendly", False)  # Default to False if missing

    return book
 
 
 
@app.get("/books/{isbn}", response_model=Book)
def get_book(isbn: str):
    book_data = db["books"].find_one({"isbn": isbn})
    if not book_data:
        raise HTTPException(status_code=404, detail="Book not found")
    return Book(**normalize_bson(book_data))


@app.get("/books/{isbn}")
def get_book_status(isbn:str):
    print("checking status from db")
    # Fetch the book from the database
    book_data = db["books"].find_one({"isbn": isbn})
    book = normalize_bson(book_data)

    status = book["status"] == "Available"
    print(f'status of book from db {status}')
    return status  # Returns True if available, False otherwise



@app.post("reserve_book")
def place_hold_db(request: Request, isbn: str):
    print("placing hold from db")
    # get user email
    # Securely get user info from session
    token = request.cookies.get("login_token")
    print("got token")
    if not token:
        return {"message": "Your session has expired. Please login again."}
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_email = payload.get("sub")
    print(f'got email {user_email}')
    if not user_email:
        return {"message": "Invalid session."}
    
    print("finding book with isbn")
    # get book instance from book db
    book = db["books"].find_one({"isbn": isbn})

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    
    # check if the same user has this copy on hold (yet to implement)
    print("placing hold to table in the db")
    # if copy is available then place hold
    reservation = {
        "reservation_id": uuid.uuid4().hex,  # Generates a random unique ID
        "book_id": uuid.uuid4().hex,  
        "user_email": user_email,
        "isbn": isbn,
        "reservation_date": datetime.utcnow().isoformat(),
        "expiration_date": (datetime.utcnow() + timedelta(days=5)).isoformat(),
        "status": "complete"
    }
    
    db["reservations"].insert_one(reservation)
    print("added to reservation")
    print("checking active holds")
    # UPDATE BOOK STATUS
    # check reservations db for active holds (reservations.status == "complete") after this addition
    active_holds = db["reservations"].count_documents({
        "isbn": isbn,
        "status": "complete"  # active hold
    })
    
    # if this is the last copy being placed on hold then change the status
    if active_holds == book["numOfCopies"]:  # Last copy taken
        db["books"].update_one({"isbn": isbn}, {"$set": {"status": "unavailable"}})

    return {"message": "Book placed on hold", "reservation": reservation}
        
        
        
@app.post("/add_to_queue")
def add_user_to_queue(isbn: str, request: Request):
        # Securely get user info from session
    token = request.cookies.get("login_token")
    
    if not token:
        return {"message": "Your session has expired. Please login again."}
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_email = payload.get("sub")
    
    if not user_email:
        return {"message": "Invalid session."}
    
    # reservation date
    reservation_date = datetime.utcnow().isoformat(),
    
    # No copies available, add to queue
    reservation = {
        "reservation_id": uuid.uuid4().hex,  # Generates a random unique ID
        "book_id": uuid.uuid4().hex,  
        "user_email": user_email,
        "isbn": isbn,
        "reservation_date": reservation_date,
        "expiration_date": (datetime.utcnow() + timedelta(days=5)).isoformat(),
        "status": "pending"
    }
    
    db["reservations"].insert_one(reservation)

    return {"message": "No copies available. You have been added to the queue.", 
            "reservation": reservation, "reservation_date": reservation_date}
    