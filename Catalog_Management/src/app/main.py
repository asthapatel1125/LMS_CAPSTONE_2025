from dotenv import load_dotenv
import uvicorn, os
from fastapi import Request, FastAPI, HTTPException, status

load_dotenv(dotenv_path='./app/config/.env')

app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,  # Use a different port
        reload=True if os.environ.get("ENVIRONMENT") == "dev" else False,
        workers=1,
    )
