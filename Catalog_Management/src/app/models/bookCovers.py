from fastapi import FastAPI
from pydantic import BaseModel
from .database.db import *
from bson import Binary
import base64

app = FastAPI()

class BookCovers(BaseModel):
    isbn: str
    imageURL: bytes
    
@app.get("/get-book-cover")
async def get_book_cover(isbn: str):
    cover = db["bookCovers"].find_one({"isbn": isbn})
    if cover:
        return cover["imageURL"]
    else:
        return None
    
@app.post("/add-book-cover")
def add_book_cover(isbn: str, image: str):
    existing_cover = db["bookCovers"].find_one({"isbn": isbn})    
    if existing_cover:
        return "Error"

    image_binary = Binary(base64.b64decode(image))
    result = db["bookCovers"].insert_one({"isbn": isbn, "imageURL": image_binary})
    if result.inserted_id:
        return "Success"
    else:
        return "Error"
    
@app.delete("/delete-book-cover")
def delete_book_cover(isbn: str):
    existing_cover = db["bookCovers"].find_one({"isbn": isbn})
    
    if existing_cover:
        result = db["bookCovers"].delete_one({"isbn": isbn})
        if result.deleted_count > 0:
            return {"message": "Book cover deleted successfully."}
        else:
            return {"message": "Error deleting book cover."}
    else:
        return {"message": "Error deleting book cover."}