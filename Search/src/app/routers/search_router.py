from fastapi import APIRouter, Form, HTTPException, status, Request
from fastapi.responses import RedirectResponse, HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates
#from controllers.authentication import *
from controllers.token import *
#from controllers.email_verif_code import *
from datetime import datetime, timedelta
import os

USER_LOGIN_PAGE = "http://127.0.0.1:8001/auth/login"
USER_LOGOUT_PAGE = "http://127.0.0.1:8001/auth/logout"

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

@router.get("/logout", response_class=HTMLResponse)
async def logout_page(request: Request):
    response = RedirectResponse(url=USER_LOGOUT_PAGE, status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("login_token")
    response.delete_cookie("user_name")
    return response