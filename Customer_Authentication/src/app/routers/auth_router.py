from fastapi import APIRouter, Form, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from controllers.authentication import *
from controllers.session import *
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, "..", "views", "templates")

templates = Jinja2Templates(directory=templates_dir)

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(uname: str = Form(...), pword: str = Form(...)):
    session_id = handle_login(uname, pword)
    response = RedirectResponse(url="/auth/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return response

# Route to handle logout
@router.post("/logout")
async def logout(session_id: str = Depends(lambda: None)):
    handle_logout(session_id)
    response = RedirectResponse(url="/auth/login")
    response.delete_cookie("session_id")
    return response

# Route to show dashboard page (after login)
@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request, session_id: str = Depends(lambda: None)):
    session = get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        )
    return templates.TemplateResponse("dashboard.html", {"request": request, "username": session["username"]})

# Route to show registration page
@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# Route to handle user registration
@router.post("/register")
async def register_user(username: str = Form(...), email: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    handle_registration(username, email, password, confirm_password)
    return RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)

# Route to show forgot password page
@router.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request})

# Route to handle password reset (mock implementation)
@router.post("/forgot-password")
async def reset_password(email: str = Form(...)):
    return handle_forgot_password(email)

# Route to validate JWT token
@router.get("/validate-token")
async def validate_token_route(token: str):
    return validate_token(token)
