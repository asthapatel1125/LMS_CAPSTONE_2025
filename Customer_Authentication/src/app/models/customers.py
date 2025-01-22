from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from .database.db import *
from typing import List, Optional

app = FastAPI()

class Address(str, Enum):
    streetAddress = "streetAddress"
    city = "city"
    state = "state"
    country = "country"

class Customer(BaseModel):
    email: str
    password: str
    firstName: str
    lastName: str
    address: List[Address]
    age: int

@app.post("/customers/", response_model=dict)
def create_user(customer: dict):
    result = db["customers"].insert_one(customer)
    return {"id": str(result.inserted_id)}

@app.get("/customers/{email}", response_model=Customer)
def get_user(email: str): 
    customer = db["customers"].find_one({"email": email})
    if not customer:
        return None
    return Customer(**customer)

@app.get("/customers/{firstName}", response_model=Customer)
async def get_user_by_fname(firstName: str):
    customer = await get_db["customers"].find_one({"firstName": firstName})
    if not customer:
        raise HTTPException(status_code=404, detail="User not found")
    return Customer(**customer)

@app.get("/customers/", response_model=List[Customer])
def list_users():
    db = get_db()
    customers = list(db["customers"].find())
    return [Customer(**customer) for customer in customers]

@app.delete("/customers/{email}")
async def delete_user(email: str):
    result = await get_db.db["customers"].delete_one({"email": email})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
