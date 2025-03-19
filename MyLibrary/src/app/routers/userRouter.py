from fastapi import APIRouter, Body, status, Request
from fastapi.responses import RedirectResponse, HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates
from controllers.token import *
from controllers.mylib import *
import os

USER_LOGIN_PAGE = "https://35.234.252.105/auth/login"
USER_SEARCH_PAGE = "https://35.234.252.105/search/home"

base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, "..", "views", "templates")
templates = Jinja2Templates(directory=templates_dir)

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
async def login_page():
    response = RedirectResponse(url=USER_LOGIN_PAGE, status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("login_token")
    response.delete_cookie("user_name")
    return response

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    name = request.cookies.get('user_name')
    return templates.TemplateResponse("myLibrary.html", {"request": request, "name": name})

@router.get("/read", response_class=HTMLResponse)
async def read_book_page(request: Request):
    return templates.TemplateResponse("read_book.html", {"request": request})


@router.get("/search", response_class=HTMLResponse)
async def search_page():
    return RedirectResponse(url=USER_SEARCH_PAGE, status_code=status.HTTP_303_SEE_OTHER)

@router.post("/completed-holds")
async def completed_holds(request: Request):
    email = get_user_email_from_token(request.cookies.get("login_token"))
    book_holds = get_completed_reservations(email)
    
    for hold in book_holds:
        temp_title = get_book_by_isbn(hold["isbn"])
        hold["title"] = temp_title
    
    return book_holds   # {ISBN, Days left, due Date, book title}

@router.post("/pending-holds")
async def pending_holds(request: Request):
    email = get_user_email_from_token(request.cookies.get("login_token"))
    book_holds = get_pending_reservations(email)
    
    for hold in book_holds:
        temp_title = get_book_by_isbn(hold["isbn"])
        hold["title"] = temp_title
    
    return book_holds   # {ISBN, Queue, Hold Date, book title}

@router.post("/wishlist")
async def get_wishlist(request: Request):
    email = get_user_email_from_token(request.cookies.get("login_token"))
    wishlist = get_wishlist_by_email(email)
    for dict in wishlist:
        temp_title = get_book_by_isbn(dict["isbn"])
        dict["title"] = temp_title
    return wishlist

@router.get("/wishlist/clear")
async def reset_wishlist(request: Request):
    email = get_user_email_from_token(request.cookies.get("login_token"))
    return clear_wishlist(email)

@router.get("/wishlist/remove/{items}")
async def wishlist_remove_items(request: Request, items: str):
    email = get_user_email_from_token(request.cookies.get("login_token"))
    items_list = items.split(",")
    for i in items_list:
        msg = delete_item_from_wishlist(email, i)
        if msg == "Error":
            return {"message": "Error deleting books from your wishlist"}
    return {"message": "Successfully deleted books from your wishlist"} 