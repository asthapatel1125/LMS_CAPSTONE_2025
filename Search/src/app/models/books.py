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


'''Search Bar Queries'''
# Get a list of books by title
@app.get("/books/{title}", response_model=List[Book])
def get_books_by_rating(title: str):
    
    return "Book List by title"


# Get a list of books by isbn (Already done above)


# Get a list of books by author
@app.get("/books/{author}", response_model=List[Book])
def get_books_by_rating(author: str):
    
    return "Book List by author"


# Get a list of books by publisher
@app.get("/books/{publisher}", response_model=List[Book])
def get_books_by_rating(publisher: str):
    
    return "Book List by publisher"



'''Filter Queries (Some can be utilized for search bar queires too)'''

# Get a list of books with ratings higher than or equal to given rating.
@app.get("/books/{rating}", response_model=List[Book])
def get_books_by_rating(rating: float):
    
    return "Popular Book List"


'''not finished'''
# Get Newest books (NOT FINISHED)
@app.get("/books/{release_date}", response_model=List[Book])
def get_latest_releases(release_date: str):
    
    return "Newely Book List"


# Get Avialable books
@app.get("/books/{status}", response_model=List[Book])
def get_books_by_status(status: str):
    
    return "Available Book List"


# Get specifically formatted items
@app.get("/books/{format}", response_model=List[Book])
def get_books_by_format(format: str):
    
    return "Specifically formatted Book List"


# Get a list of items based on a given genre
@app.get("/books/{genre}", response_model=List[Book])
def get_books_by_genre(genre: str):
    
    return "Specific genre Book List"

# Get a list of items based on the type of audience chosen
@app.get("/books/{kidFriendly}", response_model=List[Book])
def get_books_by_audience(kidFriendly: bool):
    
    return "Specific audience Book List"


# Get Book image
@app.get("/book_images/{_id}", response_model=BookImages)
def get_book_images(_id: str):
    
    return "book image object"