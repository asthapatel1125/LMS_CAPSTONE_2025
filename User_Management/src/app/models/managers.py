from fastapi import FastAPI
from pydantic import BaseModel
from .database.db import *
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

class Manager(BaseModel):
    _id: str
    managerID: str
    firstName: str
    lastName: str
    email: str
    phoneNumber: str
    address: Optional[dict]
    passwordHash: str
    
    class Config:
        json_encoders = {ObjectId: str}
    
app = FastAPI()

@app.get("/managers/", response_model=List[Manager])
def list_managers():
    db = get_db()
    managers = db["managers"].find()
    managers_list = []
    for manager in managers:
        manager["_id"] = str(manager["_id"])
        managers_list.append((manager))
    return managers_list

def manager_created_on_date(manager):
    obj_id = ObjectId(manager['_id'])
    created_on = obj_id.generation_time
    return created_on 