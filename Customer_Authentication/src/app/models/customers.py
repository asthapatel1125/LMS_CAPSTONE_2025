from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from database.db import MongoDB
from typing import List

app = FastAPI()

class Customer(BaseModel):
    email: str
    password: str
    firstName: str
    lastName: str
    address: list
    age: int

@app.post("/customers/", response_model=dict)
async def create_user(customer: Customer):
    result = await MongoDB.db["customers"].insert_one(customer.dict())
    return {"id": str(result.inserted_id)}

@app.get("/customers/{email}", response_model=Customer)
async def get_user(email: str):
    customer = await MongoDB.db["customers"].find_one({"email": ObjectId(email)})
    if not customer:
        raise HTTPException(status_code=404, detail="User not found")
    return Customer(**customer)

@app.get("/customers/{firstName}", response_model=Customer)
async def get_user_by_fname(firstname: str):
    customer = await MongoDB.db["customers"].find_one({"firstName": ObjectId(firstname)})
    if not customer:
        raise HTTPException(status_code=404, detail="User not found")
    return Customer(**customer)

@app.get("/customers/", response_model=List[Customer])
async def list_users():
    customers = await MongoDB.db["customers"].find().to_list(100)
    return [Customer(**customers) for customer in customers]

@app.delete("/customers/{email}")
async def delete_user(email: str):
    result = await MongoDB.db["customers"].delete_one({"email": ObjectId(email)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
