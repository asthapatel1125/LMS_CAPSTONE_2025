from fastapi import APIRouter, Body, status, Request, UploadFile, File
from fastapi.responses import RedirectResponse, HTMLResponse, Response, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from controllers.token import *
from controllers.notifications import *
from datetime import datetime
import os, base64
from io import BytesIO

MANAGER_LOGIN_PAGE = "https://35.234.252.105/auth/manager"
ADMIN_DASHBOARD_PAGE = "https://35.234.252.105/catalog/admin_dashboard"

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

@router.get("/admin_dashboard", response_class=HTMLResponse)
def admin_dashboard_page(response: Response):
    return RedirectResponse(url=ADMIN_DASHBOARD_PAGE, status_code=status.HTTP_303_SEE_OTHER)

@router.get("/main", response_class=HTMLResponse)
def main_page(request: Request):
    return templates.TemplateResponse("notification_center.html", {"request": request})

@router.get("/available-now")
def available_now(request: Request):
    result = handle_get_available_books()
    return result

@router.get("/returns-today")
def return_today(request: Request):
    result = handle_return_books_today()
    return result

@router.get("/return-soon")
def return_soon(request: Request):
    result = handle_return_books_soon()
    return result