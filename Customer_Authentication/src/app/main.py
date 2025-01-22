from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers.auth_router import router as auth_router
import uvicorn, os
from fastapi import Request
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from models.database.db import get_db, close_db

load_dotenv(dotenv_path='./app/config/.env')

app = FastAPI()


"""
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""

# Custom middleware example
class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print("Custom middleware: Before request processing")
        response = await call_next(request)
        print("Custom middleware: After request processing")
        return response

app.add_middleware(CustomMiddleware)

base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, "views", "static")
templates_dir = os.path.join(base_dir, "views", "templates")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

templates = Jinja2Templates(directory=templates_dir)

@app.on_event("startup")
def startup_db_client():
    try:
        # Test MongoDB connection
        get_db().client.admin.command('ping')
        print("MongoDB connected successfully!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise HTTPException(status_code=500, detail="Unable to connect to MongoDB")

@app.on_event("shutdown")
def shutdown_db_client():
    close_db()
    print("MongoDB connection closed!")


app.include_router(auth_router, prefix="/auth")

@app.get("/")
async def root(request : Request):
     return templates.TemplateResponse("login.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=8000,  # Use a different port
        reload=True if os.environ.get("ENVIRONMENT") == "dev" else False,
        workers=1,
    )
