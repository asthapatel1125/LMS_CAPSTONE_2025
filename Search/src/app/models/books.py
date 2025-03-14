from fastapi import FastAPI, APIRouter
from pydantic import BaseModel, Field, HttpUrl
from .database.db import *
from typing import List, Literal
from fastapi.responses import JSONResponse

app = FastAPI()
router = APIRouter()
db = get_db()

def normalize_bson(book: dict) -> dict:
    
    if "_id" in book:
        del book["_id"]
    """Normalize MongoDB BSON types to standard Python types."""
    fields = ["pageNumber", "numCopies", "numOfMins"]
    for field in fields:
        if isinstance(book.get(field), dict) and "$numberInt" in book[field]:
            book[field] = int(book[field]["$numberInt"])
    
    if isinstance(book.get("kidFriendly"), dict) and "$numberInt" in book["kidFriendly"]:
        book["kidFriendly"] = bool(book["kidFriendly"]["$numberInt"])
    
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
    print(f'title from models: {title}')
    books_cursor = db["books"].find({"title": {"$regex": title}})
    books = [Book(**normalize_bson(book)) for book in books_cursor]
    print(f'final books object: {books}')
    return books



# Get a list of books by isbn (Already done above)


# Get a list of books by author
@app.get("/books/{author}", response_model=List[Book])
def get_books_by_author(author: str):
    books_cursor = db["books"].find({"author": {"$regex": author}})
    books = [Book(**normalize_bson(book)) for book in books_cursor]

    return books



# Get a list of books by publisher
@app.get("/books/{publisher}", response_model=List[Book])
def get_books_by_publisher(publisher: str):
    books_cursor = db["books"].find({"publisher": {"$regex": publisher}})
    books = [Book(**normalize_bson(book)) for book in books_cursor]

    return books




'''Filter Queries (Some can be utilized for search bar queires too)'''

# Get a list of books with ratings higher than or equal to given rating.
@app.get("/books/{rating}", response_model=List[Book])
def get_books_by_rating(rating: float):
    books_cursor = db["books"].find({"rating": {"$regex": rating}})
    books = [Book(**normalize_bson(book)) for book in books_cursor]

    return books



'''not finished'''
# Get Newest books (NOT FINISHED)
@app.get("/books/{release_date}", response_model=List[Book])
def get_latest_releases(release_date: str):
    
    return book_list


# Get Avialable books
@app.get("/books/{status}", response_model=List[Book])
def get_books_by_status(status: str):
    books_cursor = db["books"].find({"status": {"$regex": status}})
    books = [Book(**normalize_bson(book)) for book in books_cursor]

    return books



# Get specifically formatted items
@app.get("/books/{format}", response_model=List[Book])
def get_books_by_format(format: str):
    books_cursor = db["books"].find({"format": {"$regex": format}})
    books = [Book(**normalize_bson(book)) for book in books_cursor]

    return books



# Get a list of items based on a given genre
@app.get("/books/{genre}", response_model=List[Book])
def get_books_by_genre(genre: str):
    books_cursor = db["books"].find({"genre": {"$regex": genre}})
    books = [Book(**normalize_bson(book)) for book in books_cursor]

    return books


# Get a list of items based on the type of audience chosen
@app.get("/books/{kidFriendly}", response_model=List[Book])
def get_books_by_audience(kidFriendly: bool):
    books_cursor = db["books"].find({"kidFriendly": {"$regex": kidFriendly}})
    books = [Book(**normalize_bson(book)) for book in books_cursor]

    return books



# Get Book image
@app.get("/book_images/{_id}", response_model=BookImages)
def get_book_images(_id: str):
    
    return book_list