from fastapi import APIRouter, Form, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse, HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from controllers.authentication import *
from controllers.token import *
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, "..", "views", "templates")

templates = Jinja2Templates(directory=templates_dir)

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(email: str = Form(), pword: str = Form()):
    jwt_token = handle_login(email, pword)
    response = RedirectResponse(url="/auth/home", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="login_token", value=jwt_token, httponly=False)
    return response

@router.get("/logout", response_class=HTMLResponse)
async def logout_page(request: Request):
    return RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)

# Route to handle logout
@router.post("/logout", response_class=HTMLResponse)
async def logout(response: Response):
    response.delete_cookie("login_token", path="/auth/login")
    response = RedirectResponse(url="/auth/login")
    return response

# Route to show registration page
@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# Route to handle user registration
@router.post("/register", response_class=HTMLResponse)
async def register_user(fname: str = Form(...), lname: str = Form(...), email: str = Form(...), password: str = Form(...), age: int = Form(...)):
    handle_registration(fname, lname, email, password, age)
    return RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)

# Route to show forgot password page
@router.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request})

# Route to handle password reset (mock implementation)
@router.post("/forgot-password")
async def reset_password(email: str = Form(...)):
    return handle_forgot_password(email)

@router.get("/home", response_class=HTMLResponse)
async def login_page(request: Request):
    return  templates.TemplateResponse("home.html", {"request": request})