from fastapi import APIRouter, Form, status, Request
from fastapi.responses import RedirectResponse, HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates
from controllers.token import *
from controllers.inventory import *
import os

MANAGER_LOGIN_PAGE = "http://127.0.0.1:8001/auth/manager"

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
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "name": manager_name})

@router.get("/manager-login", response_class=HTMLResponse)
def manager_login_page(response: Response):
    response = RedirectResponse(url=MANAGER_LOGIN_PAGE, status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("manager_login_token")
    response.delete_cookie("manager_name")
    return response

# Edit inventory page buttons (x3)

@router.get("/add-item", response_class=HTMLResponse)
def add_item_page(request: Request):
    return templates.TemplateResponse("add_book.html", {"request": request})

@router.post("/add-item", response_class=HTMLResponse)
def add_item(title: str = Form(...), isbn: str = Form(...), author: str = Form(...), genre: str = Form(...), rating: float = Form(...),
            kidFriendly: bool = Form(...), description: str = Form(...), format: str = Form(...), pageNumber: int = Form(...), 
            bookID: str = Form(...), publisher: str = Form(...), status: str = Form(...) ):
    result = handle_add_book(title, isbn, author, genre, rating, kidFriendly, description, format, pageNumber, bookID, publisher, status)
    if result == "Error":
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Item already exists."}
        )
    return RedirectResponse(url="/catalog/edit_inventory", status_code=status.HTTP_303_SEE_OTHER)

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