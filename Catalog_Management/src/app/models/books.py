from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
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

# Create books
@app.post("/books/", response_model=dict)
def create_book(book: Book):
    book_dict = book.dict()
    result = db["books"].insert_one(book_dict)
    return {"id": str(result.inserted_id)}

# Get book information
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

# Delete entire book
@app.delete("/books/{isbn}", response_model=dict)
def delete_book(isbn: str):
    result = db["books"].delete_one({"isbn": isbn})
    if result.deleted_count == 1:
        return {"message": "Book deleted successfully."}
    else:
        return {"message": "Error deleting book."}
    
# Update any field of the book (total 11 fields, excluding bookID)
@app.put("/catalog/update-isbn/{book_id}", response_model=dict)
def update_isbn(book_id: str, new_isbn: str):
    result = db["books"].update_one(
        {"bookID": book_id},
        {"$set": {"isbn": new_isbn}}
    )
    return result.modified_count > 0

@app.put("/catalog/update-title/{book_id}", response_model=dict)
def update_title(book_id: str, new_title: str):
    result = db["books"].update_one(
        {"bookID": book_id},
        {"$set": {"title": new_title}}
    )
    return result.modified_count > 0

@app.put("/catalog/update-description/{book_id}", response_model=dict)
def update_description(book_id: str, new_description: str):
    result = db["books"].update_one(
        {"bookID": book_id},
        {"$set": {"description": new_description}}
    )
    return result.modified_count > 0

@app.put("/catalog/update-rating/{book_id}", response_model=dict)
def update_rating(book_id: str, new_rating: float):
    result = db["books"].update_one(
        {"bookID": book_id},
        {"$set": {"rating": new_rating}}
    )
    return result.modified_count > 0

@app.put("/catalog/update-author/{book_id}", response_model=dict)
def update_author(book_id: str, new_author: str):
    result = db["books"].update_one(
        {"bookID": book_id},
        {"$set": {"author": new_author}}
    )
    return result.modified_count > 0

@app.put("/catalog/update-genre/{book_id}", response_model=dict)
def update_genre(book_id: str, new_genre: str):
    result = db["books"].update_one(
        {"bookID": book_id},
        {"$set": {"genre": new_genre}}
    )
    return result.modified_count > 0

@app.put("/catalog/update-kidFriendly/{book_id}", response_model=dict)
def update_kidFriendly(book_id: str, new_kidFriendly: bool):
    result = db["books"].update_one(
        {"bookID": book_id},
        {"$set": {"kidFriendly": new_kidFriendly}}
    )
    return result.modified_count > 0

@app.put("/catalog/update-format/{book_id}", response_model=dict)
def update_format(book_id: str, new_format: str):
    result = db["books"].update_one(
        {"bookID": book_id},
        {"$set": {"format": new_format}}
    )
    return result.modified_count > 0

@app.put("/catalog/update-pageNumber/{book_id}", response_model=dict)
def update_pageNumber(book_id: str, new_pageNumber: int):
    result = db["books"].update_one(
        {"bookID": book_id},
        {"$set": {"pageNumber": new_pageNumber}}
    )
    return result.modified_count > 0

@app.put("/catalog/update-publisher/{book_id}", response_model=dict)
def update_publisher(book_id: str, new_publisher: str):
    result = db["books"].update_one(
        {"bookID": book_id},
        {"$set": {"publisher": new_publisher}}
    )
    return result.modified_count > 0

@app.put("/catalog/update-status/{book_id}", response_model=dict)
def update_status(book_id: str, new_status: str):
    result = db["books"].update_one(
        {"bookID": book_id},
        {"$set": {"status": new_status}}
    )
    return result.modified_count > 0


