from fastapi import APIRouter, Form, HTTPException, status, Request
from fastapi.responses import RedirectResponse, HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates
from controllers.token import *
from datetime import datetime, timedelta
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, "..", "views", "templates")
templates = Jinja2Templates(directory=templates_dir)

router = APIRouter()

@router.get("/edit_inventory", response_class=HTMLResponse)
def edit_inventory_page(request: Request):
    return templates.TemplateResponse("edit_inventory.html", {"request": request})
