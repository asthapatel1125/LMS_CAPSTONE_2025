from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

    @staticmethod
    @asynccontextmanager
    async def lifespan():
        MongoDB.client = AsyncIOMotorClient(MONGO_URI)
        MongoDB.db = MongoDB.client[DATABASE_NAME]
        print(f"Connected to the database: {DATABASE_NAME}")

        yield

        if MongoDB.client:
            MongoDB.client.close()
            print("Database connection is closed.")
