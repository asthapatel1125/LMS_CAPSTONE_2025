from fastapi import FastAPI, APIRouter
from pydantic import BaseModel, HttpUrl
from .database.db import *
from typing import List
from fastapi.responses import JSONResponse

app = FastAPI()
router = APIRouter()

class Book(BaseModel):
    title: str
    isbn: str
    author: str
    genre: str
    rating: float
    kidFriendly: bool
    description: str
    format: str
    pageNumber: int
    bookID: str
    publisher: str
    status: str

class BookImages(BaseModel):
    _id: str
    bookISBN: str
    imageURL: HttpUrl

@app.get("/books/{isbn}", response_model=Book)
def get_book(isbn: str):
    book = db["books"].find_one({"isbn": isbn})
    if not book:
        return None
    book["_id"] = str(book["_id"])

    if isinstance(book["pageNumber"], dict) and "$numberInt" in book["pageNumber"]:
        book["pageNumber"] = int(book["pageNumber"]["$numberInt"])
    if isinstance(book["rating"], dict) and "$numberInt" in book["rating"]:
        book["rating"] = float(book["rating"]["$numberInt"])
    if isinstance(book['kidFriendly'], dict) and "$numberInt" in book['kidFriendly']:
        book['kidFriendly'] = bool(book['kidFriendly']["$numberInt"])

    return Book(**book)

@router.get("/books", response_model=List[Book])
def list_books():
    db = get_db()
    books = list(db["books"].find())
    return [Book(**book) for book in books]
