from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from .database.db import *
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

app = FastAPI()

class Address(BaseModel):
    streetAddress: str
    city: str
    state: str
    country: str

class Customer(BaseModel):
    _id: str
    email: str
    password: str
    firstName: str
    lastName: str
    address: Address
    age: int
    
    class Config:
        json_encoders = {ObjectId: str}
    
@app.post("/customers/", response_model=dict)
def create_user(customer: Customer):
    customer_dict = customer.dict()
    result = db["customers"].insert_one(customer_dict)
    return {"id": str(result.inserted_id)}

@app.get("/customers/")
def list_users():
    db = get_db()
    customers = db["customers"].find()
    customers_list = []
    for customer in customers:
        customer["_id"] = str(customer["_id"])
        customers_list.append((customer))
    return customers_list

def customer_created_on_date(customer):
    obj_id = ObjectId(customer["_id"])
    created_on = obj_id.generation_time
    return created_on

