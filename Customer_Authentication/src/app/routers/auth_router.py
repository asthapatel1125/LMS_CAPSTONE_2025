from fastapi import APIRouter, Form, HTTPException, status, Request
from fastapi.responses import RedirectResponse, HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates
from controllers.authentication import *
from controllers.token import *
from datetime import datetime, timedelta
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
    
    if jwt_token:
        expiration_time = datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRATION_TIME)
        expires = expiration_time.strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        response = RedirectResponse(url="/auth/home", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="login_token", value=jwt_token, httponly=True, expires=expires, max_age=TOKEN_EXPIRATION_TIME)
        return response
    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid username or password"}
        )

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
@router.post("/forgot-password", response_class=HTMLResponse)
async def forgot_password(email: str = Form(...)):
    if handle_forgot_password(email):
        return RedirectResponse(url="/auth/verification-code", status_code=status.HTTP_303_SEE_OTHER)
    raise HTTPException(status_code=400, detail="Email is not registered.")    

@router.get("/home", response_class=HTMLResponse)
async def login_page(request: Request):
    return  templates.TemplateResponse("home.html", {"request": request})

# load verification code page
@router.get("/verification-code", response_class=HTMLResponse)
async def verification_code_page(request: Request):
    return templates.TemplateResponse("verification_code.html", {"request": request})

@router.post("/verification-code", response_class=HTMLResponse)
async def verification_code():
    return RedirectResponse(url="/auth/reset-password", status_code=status.HTTP_303_SEE_OTHER)

# load verification code page
@router.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page(request: Request):
    return templates.TemplateResponse("reset_password.html", {"request": request})

# Route to show forgot password page
@router.get("/manager", response_class=HTMLResponse)
async def manager_login_page(request: Request):
    return templates.TemplateResponse("manager_login.html", {"request": request})

# Route to handle password reset (mock implementation)
@router.post("/manager")
async def reset_password(userId: str = Form(...), password: str = Form(...)):
    # handle_manager_login(userId, password)
    return RedirectResponse(url = "/auth/admin_dashboard", status_code = status.HTTP_303_SEE_OTHER)

@router.get("/admin_dashboard", response_class = HTMLResponse)
async def get_admin_dashboard(request: Request):
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})