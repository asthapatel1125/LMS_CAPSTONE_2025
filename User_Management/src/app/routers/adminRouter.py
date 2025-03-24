from fastapi import APIRouter, Body, status, Request
from fastapi.responses import RedirectResponse, HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from controllers.token import *
from controllers.user_controller import *

MANAGER_LOGIN_PAGE = "https://35.234.252.105/auth/manager"

base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, "..", "views", "templates")
templates = Jinja2Templates(directory=templates_dir)

router = APIRouter()

@router.get("/main", response_class=HTMLResponse)
def main_page(request: Request):
    manager_name = request.cookies.get("manager_name", "Admin")
    return templates.TemplateResponse("manage_users_main.html", {"request": request, "manager": manager_name})

@router.get("/manager-login", response_class=HTMLResponse)
def manager_login_page(response: Response):
    response = RedirectResponse(url=MANAGER_LOGIN_PAGE, status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("manager_login_token")
    response.delete_cookie("manager_name")
    return response

@router.get("/all-users")
def get_all_users(request: Request):
    return handle_get_users()

@router.get("/add-user")
def add_user_page(email: str, request: Request):
    return templates.TemplateResponse("add_user.html", {"request": request})

@router.get("/edit-user/{email}")
def modify_user_page(email: str, request: Request):
    return templates.TemplateResponse("edit_profile.html", {"request": request})

@router.get("/delete-user/{email}")
def delete_user_page(email: str, request: Request):
    return templates.TemplateResponse("delete_user.html", {"request": request})
