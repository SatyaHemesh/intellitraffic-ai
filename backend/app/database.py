# backend/app/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import logging

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def connect_to_mongo():
    try:
        db.client = AsyncIOMotorClient(settings.MONGODB_URL)
        logging.info(f"Connected to MongoDB at {settings.MONGODB_URL}")
    except Exception as e:
        logging.error(f"Could not connect to MongoDB: {e}")

async def close_mongo_connection():
    if db.client:
        db.client.close()
        logging.info("Closed MongoDB connection")

def get_database():
    return db.client[settings.DATABASE_NAME]