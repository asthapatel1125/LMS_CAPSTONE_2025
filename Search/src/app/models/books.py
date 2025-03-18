from datetime import datetime
from bson import ObjectId
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel, Field, HttpUrl, field_validator
from .database.db import *
from typing import List, Literal
from fastapi.responses import JSONResponse

app = FastAPI()
router = APIRouter()
db = get_db()

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

class BookImages(BaseModel):
    _id: str
    bookISBN: str
    imageURL: HttpUrl
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
        
book_list = [
        Book(
            title="The Great Adventure",
            author="John Doe",
            genre="Adventure",
            rating=4,
            kidFriendly=True,
            description="A thrilling journey through uncharted territories.",
            format="Hardcover",
            pageNumber=300,
            publisher="Adventure Press",
            status="Available",
            isbn="123-456-7890",
            numOfMins=360,
            numCopies=10
        )
    ]

@app.get("/books/{isbn}", response_model=List[Book])
def get_book(isbn: str):
    
    books_cursor = db["books"].find({"isbn": isbn})
    books = [Book(**normalize_bson(book)) for book in books_cursor]

    return books

@router.get("/books", response_model=List[Book])
def list_books():
    db = get_db()
    books = list(db["books"].find())
    return [Book(**book) for book in books]


'''Search Bar Queries'''
# Get a list of books by title
@app.get("/books/{title}", response_model=List[Book])
def get_books_by_title(title: str):
    # Adding the 'i' flag for case-insensitive matching
    books_cursor = db["books"].find({"title": {"$regex": title, "$options": "i"}})
    books = [Book(**normalize_bson(book)) for book in books_cursor]
    return books


# Get a list of books by author
@app.get("/books/{author}", response_model=List[Book])
def get_books_by_author(author: str):
    # Adding the 'i' flag for case-insensitive matching
    books_cursor = db["books"].find({"author": {"$regex": author, "$options": "i"}})
    books = [Book(**normalize_bson(book)) for book in books_cursor]
    return books

# Get a list of books with a rating greater than or equal to the given rating
@app.get("/books/rating/{rating}", response_model=List[Book])
def get_books_by_rating(rating: float):
    # Adding the 'i' flag for case-insensitive matching isn't necessary for numeric comparisons
    books_cursor = db["books"].find({"rating": {"$gte": rating}})
    books = [Book(**normalize_bson(book)) for book in books_cursor]
    return books

# Get a list of books by publisher
@app.get("/books/{publisher}", response_model=List[Book])
def get_books_by_publisher(publisher: str):
    # Adding the 'i' flag for case-insensitive matching
    books_cursor = db["books"].find({"publisher": {"$regex": publisher, "$options": "i"}})
    books = [Book(**normalize_bson(book)) for book in books_cursor]
    return books


# Get a list of books by genre
@app.get("/books/{genre}", response_model=List[Book])
def get_books_by_genre(genre: str):
    # Adding the 'i' flag for case-insensitive matching
    books_cursor = db["books"].find({"genre": {"$regex": genre, "$options": "i"}})
    books = [Book(**normalize_bson(book)) for book in books_cursor]
    return books


# Get a list of books by status
@app.get("/books/{status}", response_model=List[Book])
def get_books_by_status(status: str):
    # Adding the 'i' flag for case-insensitive matching
    books_cursor = db["books"].find({"status": {"$regex": status, "$options": "i"}})
    books = [Book(**normalize_bson(book)) for book in books_cursor]
    return books


# Get a list of books by format
@app.get("/books/{format}", response_model=List[Book])
def get_books_by_format(format: str):
    # Adding the 'i' flag for case-insensitive matching
    books_cursor = db["books"].find({"format": {"$regex": format, "$options": "i"}})
    books = [Book(**normalize_bson(book)) for book in books_cursor]
    return books


# Get a list of books by audience (kid-friendly)
@app.get("/books/{kidFriendly}", response_model=List[Book])
def get_books_by_audience(kidFriendly: bool):
    # Adding the 'i' flag for case-insensitive matching if the field is a string
    books_cursor = db["books"].find({"kidFriendly": {"$regex": str(kidFriendly), "$options": "i"}})
    books = [Book(**normalize_bson(book)) for book in books_cursor]
    return books


# Get Book image
@app.get("/book_images/{bookISBN}", response_model=BookImages)
def get_book_images(bookISBN: str):
    return book_list
