from fastapi import FastAPI
from pydantic import BaseModel
from .database.db import *
from bson import Binary
import base64

app = FastAPI()

class digitalMaterial(BaseModel):
    isbn: str
    file: bytes

@app.post("/add-book-file")
def add_book_file(isbn: str, bookFile: str):
    existing_file = db["digitalMaterial"].find_one({"isbn": isbn})    
    if existing_file:
        return "Error"

    file_binary = Binary(base64.b64decode(bookFile))
    result = db["digitalMaterial"].insert_one({"isbn": isbn, "file": file_binary})
    if result.inserted_id:
        return "Success"
    else:
        return "Error"
    
@app.delete("/delete-book-file")
def delete_book_file(isbn: str):
    existing_file = db["digitalMaterial"].find_one({"isbn": isbn})
    
    if existing_file:
        result = db["digitalMaterial"].delete_one({"isbn": isbn})
        if result.deleted_count > 0:
            return {"message": "Book file deleted successfully."}
        else:
            return {"message": "Error deleting book file."}
    else:
        return {"message": "Error deleting book file."}