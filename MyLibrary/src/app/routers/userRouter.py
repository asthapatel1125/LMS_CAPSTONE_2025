from fastapi import APIRouter, Body, status, Request
from fastapi.responses import RedirectResponse, HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates
from controllers.token import *
from controllers.mylib import *
import os

USER_LOGIN_PAGE = "http://127.0.0.1:8001/auth/login"
USER_SEARCH_PAGE = "http://127.0.0.1:8003/search/home"

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
    return templates.TemplateResponse("myLibrary.html", {"request": request})

@router.get("/search", response_class=HTMLResponse)
async def search_page():
    return RedirectResponse(url=USER_SEARCH_PAGE, status_code=status.HTTP_303_SEE_OTHER)