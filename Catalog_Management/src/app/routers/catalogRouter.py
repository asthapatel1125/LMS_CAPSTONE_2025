from fastapi import APIRouter, Body, status, Request
from fastapi.responses import RedirectResponse, HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates
from controllers.token import *
from controllers.inventory import *
from datetime import datetime
import os

MANAGER_LOGIN_PAGE = "http://127.0.0.1:8001/auth/manager"
MANAGE_HOLDS_ADMIN = "http://127.0.0.1:8004/reservations/holds-admin"

base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, "..", "views", "templates")
templates = Jinja2Templates(directory=templates_dir)

router = APIRouter()

@router.get("/edit_inventory", response_class=HTMLResponse)
def edit_inventory_page(request: Request):
    return templates.TemplateResponse("edit_inventory.html", {"request": request})

@router.get("/admin_dashboard", response_class=HTMLResponse)
def admin_dashboard_page(request: Request):
    manager_name = request.cookies.get("manager_name", "Admin")
    curHr = datetime.now().hour
    # Determine greeting
    if 0 <= curHr < 12:
        greeting = f"Good Morning {manager_name} 🖥️"
    elif 12 <= curHr < 17:
        greeting = f"Good Afternoon {manager_name} 🖥️"
    else:
        greeting = f"Good Evening {manager_name} 🖥️"
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "greeting": greeting})

@router.get("/manager-login", response_class=HTMLResponse)
def manager_login_page(response: Response):
    response = RedirectResponse(url=MANAGER_LOGIN_PAGE, status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("manager_login_token")
    response.delete_cookie("manager_name")
    return response

# Manage holds page button

@router.get("/manage-holds", response_class=HTMLResponse)
def manage_holds_page(response: Response):
    return RedirectResponse(url=MANAGE_HOLDS_ADMIN, status_code=status.HTTP_303_SEE_OTHER)

# Edit inventory page buttons (x3)

@router.get("/add-item", response_class=HTMLResponse)
def add_item_page(request: Request):
    return templates.TemplateResponse("add_book.html", {"request": request})

@router.post("/add-item", response_class=HTMLResponse)
def add_item(title: str = Body(...), isbn: str = Body(...), author: str = Body(...), genre: str = Body(...), rating: float = Body(...),
            kidFriendly: bool = Body(...), description: str = Body(...), format: str = Body(...), pageNumber: int = Body(...), 
            bookID: str = Body(...), publisher: str = Body(...), status: str = Body(...) ):
    result = handle_add_book(title, isbn, author, genre, rating, kidFriendly, description, format, pageNumber, bookID, publisher, status)
    if result == "Error":
        return JSONResponse(
            status_code=409,
            content={"detail": "Item already exists."}
        )
    return RedirectResponse(url="/catalog/edit_inventory", status_code=303)

@router.get("/remove-item", response_class=HTMLResponse)
def remove_item_page(request: Request):
    books = list_books()
    return templates.TemplateResponse("delete_book.html", {"request": request, "books": books})

@router.get("/books/", response_model=List[Book])
def list_books_json():
    books = list_books()
    return JSONResponse(content=[book.dict() for book in books])

@router.get("/books/{isbn}", response_model=dict)
def delete_book_request(isbn: str):
    result = delete_book(isbn)
    return result

@router.get("/modify-item", response_class=HTMLResponse)
def modify_item_page(request: Request):
    return templates.TemplateResponse("modify_book.html", {"request": request})

@router.post("/modify-item", response_class=HTMLResponse)
def modify_item(title: str = Body(...), isbn: str = Body(...), author: str = Body(...), genre: str = Body(...),
                rating: float = Body(...), description: str = Body(...), kidFriendly: bool = Body(...),
                format: str = Body(...), pageNumber: int = Body(...), publisher: str = Body(...), status: str = Body(...)):
    
    result = handle_modify_book(title, isbn, author, genre, rating, description, kidFriendly, format, pageNumber, publisher, status)
    if result == False:
        return JSONResponse(
            status_code=409,
            content={"detail": "Nothing has been updated."}
        )
    return RedirectResponse(url="/catalog/edit_inventory", status_code=200)