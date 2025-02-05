from fastapi import APIRouter, Form, HTTPException, status, Request
from fastapi.responses import RedirectResponse, HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates
from controllers.authentication import *
from controllers.token import *
from controllers.email_verif_code import *
from datetime import datetime, timedelta
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, "..", "views", "templates")

templates = Jinja2Templates(directory=templates_dir)

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    login_token = request.cookies.get("login_token")
    if login_token:
        try:
            verify_jwt(login_token)
            return RedirectResponse(url="/auth/home", status_code=status.HTTP_303_SEE_OTHER)
        except HTTPException:
            pass
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(email: str = Form(), pword: str = Form()):
    jwt_token = handle_login(email, pword) 
    if jwt_token:
        expiration_time = datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRATION_TIME)
        expires = expiration_time.strftime('%a, %d %b %Y %H:%M:%S GMT')
        response = RedirectResponse(url="/auth/home", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="login_token", value=jwt_token, httponly=True, expires=expires, max_age=TOKEN_EXPIRATION_TIME)
        
        user = get_user(email)
        user_name = user.firstName if user else "Guest"
        response.set_cookie(key="user_name", value=user_name, httponly=True, expires=expires, max_age=TOKEN_EXPIRATION_TIME)
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
    response = RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("login_token")
    response.delete_cookie("user_name")
    return response

# Route to show registration page
@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# Route to handle user registration
@router.post("/register")
async def register_user(fname: str = Form(...), lname: str = Form(...), email: str = Form(...), password: str = Form(...), age: int = Form(...)):
    result = handle_registration(fname, lname, email, password, age)
    if result == "Error":
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Email is already registered."}
        )
    return RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)

# Route to show forgot password page
@router.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request})

# Route to handle password reset
@router.post("/forgot-password", response_class=HTMLResponse)
async def forgot_password(response: Response, request: Request, email: str = Form(...)):
    if handle_forgot_password(email):
        expiration_time = datetime.utcnow() + timedelta(minutes=10)
        expires = expiration_time.strftime('%a, %d %b %Y %H:%M:%S GMT')
        verif_code = generate_code()
        code_token = generate_code_token(verif_code, expiration_time) 
        
        response = RedirectResponse(url="/auth/verification-code", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="verif_code", value=code_token, httponly=True, expires=expires, max_age=TOKEN_EXPIRATION_TIME)
        response.set_cookie(key="verif_email", value=email, httponly=True, expires=expires, max_age=TOKEN_EXPIRATION_TIME)
        
        send_verif_email(email, verif_code)
        return response
    
    return templates.TemplateResponse("forgot_password.html", {"request": request, "error": "Email is not registered."})   

@router.get("/home", response_class=HTMLResponse)
async def login_page(request: Request):
    user_name = request.cookies.get("user_name", "Guest")
    return templates.TemplateResponse("home.html", {"request": request, "name": user_name})

@router.get("/verification-code", response_class=HTMLResponse)
async def verification_code_page(request: Request):
    return templates.TemplateResponse("verification_code.html", {"request": request})

@router.post("/verification-code", response_class=HTMLResponse)
async def verification_code(request: Request, code: int = Form(...)):
    isValid = validate_code(request, code)
    if isValid:
        response = RedirectResponse(url="/auth/reset-password", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("verif_code")
        return response
    return templates.TemplateResponse("verification_code.html", {"request": request, "error": "Invalid verification code."})

@router.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page(request: Request):
    return templates.TemplateResponse("reset_password.html", {"request": request})

@router.post("/reset_password", response_class=HTMLResponse)
async def verification_code(request: Request, first: str = Form(...), second: str = Form(...)):
    result = handle_reset_password(request, first, second)
    if result:
        response = templates.TemplateResponse("reset_password.html", {"request": request, "success": "Password has been changed."})
        response.delete_cookie("verif_email")
        return response
    return JSONResponse(
            status_code=400,
            content={"error": "Passwords do not match"}
        )


# Manager login routes

@router.get("/manager", response_class=HTMLResponse)
async def manager_login_page(request: Request):
    return templates.TemplateResponse("manager_login.html", {"request": request})

@router.post("/manager")
def manager_login(manager_id: str = Form(), password: str = Form()):
    jwt_token = handle_manager_login(manager_id, password)
    
    if jwt_token:
        expiration_time = datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRATION_TIME)
        expires = expiration_time.strftime('%a, %d %b %Y %H:%M:%S GMT')
        # to be changed
        response = RedirectResponse(url="/catalog/", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="manager_login_token", value=jwt_token, httponly=True, expires=expires, max_age=TOKEN_EXPIRATION_TIME)

        manager = get_manager(manager_id)
        manager_name = manager.firstName if manager else "Manager"
        response.set_cookie(key="manager_name", value=manager_name, httponly=True, expires=expires, max_age=TOKEN_EXPIRATION_TIME)

        return response
    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid manager ID or password"}
        )

@router.get("/admin_dashboard", response_class = HTMLResponse)
async def get_admin_dashboard(request: Request):
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})