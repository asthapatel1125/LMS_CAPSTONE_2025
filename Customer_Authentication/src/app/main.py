from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn, os
from models.database.db import get_db, close_db
from routers.auth_router import router as auth_router

# Load environment variables
load_dotenv(dotenv_path="./app/config/.env")

# FastAPI app setup
app = FastAPI()

# Middleware definition
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity (modify as needed)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With", "Accept"],
)

# Directories for static files and templates
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
    
# Include additional routers here (example: auth_router)
# from routers.auth_router import router as auth_router
app.include_router(auth_router, prefix="/auth")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        reload=True if os.environ.get("ENVIRONMENT") == "dev" else False,
        workers=1,
    )