from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from controllers.routers import router as auth_router
import uvicorn
import os

app = FastAPI()

base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, "views", "static")
templates_dir = os.path.join(base_dir, "views", "templates")

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

app.include_router(auth_router, prefix="/authentication")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
