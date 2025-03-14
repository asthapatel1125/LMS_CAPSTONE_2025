import json
from fastapi import APIRouter, Form, HTTPException, status, Request
from fastapi.responses import RedirectResponse, HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates
from controllers.search_controller import *
from controllers.token import *
from models.books import *  
from models.filters import *
from datetime import datetime, timedelta
import os
from pydantic import BaseModel, HttpUrl

USER_LOGIN_PAGE = "https://35.234.252.105/auth/login"
USER_LOGOUT_PAGE = "https://35.234.252.105/auth/logout"
MYLIBRARY_PAGE = "https://35.234.252.105/mylib/dashboard"

base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, "..", "views", "templates")
templates = Jinja2Templates(directory=templates_dir)

router = APIRouter()

@router.get("/home", response_class=HTMLResponse)
def home_page(request: Request):
    user_name = request.cookies.get("user_name", "Guest")
    return templates.TemplateResponse("search_page.html", {"request": request, "name": user_name})

@router.get("/item-info", response_class=HTMLResponse)
def item_info_page(request: Request):
    return templates.TemplateResponse("item_info.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return RedirectResponse(url=USER_LOGIN_PAGE, status_code=status.HTTP_303_SEE_OTHER)

@router.get("/mylibrary", response_class=HTMLResponse)
async def login_page(request: Request):
    return RedirectResponse(url=MYLIBRARY_PAGE, status_code=status.HTTP_303_SEE_OTHER)

@router.get("/logout", response_class=HTMLResponse)
async def logout_page(request: Request):
    response = RedirectResponse(url=USER_LOGOUT_PAGE, status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("login_token")
    response.delete_cookie("user_name")
    return response


@router.get("/searchQuery", response_class=JSONResponse)
async def search_query_page(request: Request, query: str):
    print(query)
    # Call the method to retrieve books based on the search query
    results = retrieve_searchQuery_list(query)
    search_results = [{
        "title": book.title,
        "author":book.author,
        "genre": book.genre,
        "rating": book.rating,
        "kidFriendly": book.kidFriendly,
        "description":  book.description,
        "format": book.format,
        "pageNumber":  book.pageNumber,
        "publisher":  book.publisher,
        "status":  book.status,
        "isbn": book.isbn,
        "numOfMins": book.numOfMins,
        "numCopies": book.numCopies
    } for book in results]

    if not results:
        return JSONResponse(content={"message": "No books found matching your search."}, status_code=status.HTTP_404_NOT_FOUND)
    
    # Return books as JSON data
    return JSONResponse(content={"books": search_results})

@router.get("/popular", response_class=JSONResponse)
async def get_popular_books():
    
    # Popular books: Ratings highter than or equal to 5 stars
    results = get_books_by_rating(4.5)
    popular_books = [{
        "title": book.title,
        "author":book.author,
        "genre": book.genre,
        "rating": book.rating,
        "kidFriendly": book.kidFriendly,
        "description":  book.description,
        "format": book.format,
        "pageNumber":  book.pageNumber,
        "publisher":  book.publisher,
        "status":  book.status,
        "isbn": book.isbn,
        "numOfMins": book.numOfMins,
        "numCopies": book.numCopies
    } for book in results]
    return JSONResponse(content={"popular_books": popular_books})

@router.get("/newest", response_class=JSONResponse)
async def get_newest_books():
    
    # Newest books: Latest releases 
    results = retrieve_newest_books()
    newest_books = [{
        "title": book.title,
        "author":book.author,
        "genre": book.genre,
        "rating": book.rating,
        "kidFriendly": book.kidFriendly,
        "description":  book.description,
        "format": book.format,
        "pageNumber":  book.pageNumber,
        "publisher":  book.publisher,
        "status":  book.status,
        "isbn": book.isbn,
        "numOfMins": book.numOfMins,
        "numCopies": book.numCopies
    } for book in results]
    
    return JSONResponse(content={"newest_books": newest_books})


@router.get("/search_result_page", response_class=HTMLResponse)
async def get_search_result_page(request: Request, query: str):
    # Pass the query to the HTML template (if present)
    print(f'search_result_page query value:',query)
    return templates.TemplateResponse("search_result_page.html", {"request": request, "query": query})
    
    
'''Filtered queries'''
# Define the endpoint to receive filters and return filtered books
@router.post("/filter_books", response_class=JSONResponse)
async def filter_books(filters: FilterRequest):
    print(f'filters query:',filters.searchQuery)
    books = retrieve_searchQuery_list(filters.searchQuery)
    # books = retrieve_searchQuery_list(filters.searchQuery)
    # Filter the books based on the given filters
    filtered_books = [book for book in books if
                      (not filters.genres or book.genre in filters.genres) and
                      (not filters.formats or book.format in filters.formats) and
                      (not filters.availability or book.numCopies > 0) and
                      (not filters.audience or book.kidFriendly in filters.audience) and
                      (not filters.ratings or book.rating in filters.ratings)]

    # If no books match the filters, return an empty list
    if not filtered_books:
        return JSONResponse(content=[], status_code=200)

    # Convert the filtered books to a dictionary that can be returned as JSON
    books_list = [{
        "title": book.title,
        "author":book.author,
        "genre": book.genre,
        "rating": book.rating,
        "kidFriendly": book.kidFriendly,
        "description":  book.description,
        "format": book.format,
        "pageNumber":  book.pageNumber,
        "publisher":  book.publisher,
        "status":  book.status,
        "isbn": book.isbn,
        "numOfMins": book.numOfMins,
        "numCopies": book.numCopies
    } for book in filtered_books]

    # Return the filtered books as a JSONResponse
    return JSONResponse(content=books_list, status_code=200)


@router.get("/book_info/{isbn}", response_class=HTMLResponse)
async def get_book_info(isbn: str):
    # book_info = get_book(isbn)
    book_info = {
        "coverImage": "https://via.placeholder.com/150",
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "year": "1925",
        "isbn": "ASDBU1273712UGFSD",
        "format": "EPUB",
        "synopsis": "The Great Gatsby, F. Scott Fitzgerald’s third book, stands as the supreme achievement of his career. First published by Scribner in 1925, this quintessential novel of the Jazz Age has been acclaimed by generations of readers. The story of the mysteriously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan is an exquisitely crafted tale of America in the 1920s.",
        "reviews": [
            {"user": "Alice", "rating": 5, "text": "Loved it! A timeless classic."},
            {"user": "Bob", "rating": 4, "text": "Great book with deep themes."},
            {"user": "Charlie", "rating": 3, "text": "Interesting but not my style."}
        ],
        "copies": 5
    }
    return JSONResponse(content={"book_info": book_info})

@router.get("/book_info", response_class=HTMLResponse)
async def get_book_info_page(request: Request, isbn: str):
    # Pass the query to the HTML template (if present)
    print(f'isbn from book_info', isbn)
    return templates.TemplateResponse("book_info.html", {"request": request, "isbn": isbn})

@router.post("/place_hold")
async def place_hold(request: Request, book: Book):
    
    return ""