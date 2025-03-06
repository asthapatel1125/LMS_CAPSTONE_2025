from fastapi import APIRouter, Body, status, Request
from fastapi.responses import RedirectResponse, HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates
from controllers.token import *
from controllers.holds import *
import os

MANAGER_LOGIN_PAGE = "http://127.0.0.1:8001/auth/manager"
ADMIN_LOGOUT_PAGE = "http://127.0.0.1:8001/auth/manager-logout"
ADMIN_DASHBOARD_PAGE = "http://127.0.0.1:8002/catalog/admin_dashboard"

base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, "..", "views", "templates")
templates = Jinja2Templates(directory=templates_dir)

router = APIRouter()

@router.get("/manager-login", response_class=HTMLResponse)
def manager_login_page(response: Response):
    response = RedirectResponse(url=MANAGER_LOGIN_PAGE, status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("manager_login_token")
    response.delete_cookie("manager_name")
    return response

@router.get("/holds-admin", response_class=HTMLResponse)
def holds_admin_page(request: Request):
    return templates.TemplateResponse("manage_holds_admin.html", {"request": request})

@router.post("/logout", response_class=HTMLResponse)
async def logout(response: Response):
    response = RedirectResponse(url=ADMIN_LOGOUT_PAGE, status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("manager_login_token")
    response.delete_cookie("manager_name")
    return response

@router.post("/dashboard", response_class=HTMLResponse)
async def dashboard(response: Response):
    response = RedirectResponse(url=ADMIN_DASHBOARD_PAGE, status_code=status.HTTP_303_SEE_OTHER)
    return response

# Filling the table in Manage Holds page
@router.get("/list-holds/", response_model=List[Reservations])
def list_holds_json():
    holds = list_holds()
    return JSONResponse(content=[hold.dict() for hold in holds])

# Getting the book title from the database
@router.get("/book-title/{isbn}", response_model=dict)
def book_title_json(isbn: str):
    title = get_book_title(isbn)
    if title == "Book not found":
        return JSONResponse(status_code=404, content={"message": title})
    return JSONResponse(content={"title": title})

