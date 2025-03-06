from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from .database.db import *
from typing import List
from fastapi.responses import JSONResponse

app = FastAPI()

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

@app.post("/books/", response_model=dict)
def create_book(book: Book):
    book_dict = book.dict()
    result = db["books"].insert_one(book_dict)
    return {"id": str(result.inserted_id)}

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

@app.get("/books/", response_model=List[Book])
def list_books():
    db = get_db()
    books = list(db["books"].find())
    return [Book(**book) for book in books]

@app.get("/books/title/{isbn}", response_model=str)
def get_book_title(isbn: str):
    db = get_db()
    book = db["books"].find_one({"isbn": isbn}, {"_id": 0, "title": 1})
    if not book:
        return "Book not found"
    return book["title"]

@app.delete("/books/{isbn}", response_model=dict)
def delete_book(isbn: str):
    result = db["books"].delete_one({"isbn": isbn})
    if result.deleted_count == 1:
        return {"message": "Book deleted successfully."}
    else:
        return {"message": "Error deleting book."}
