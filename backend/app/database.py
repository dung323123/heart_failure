from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URL, DATABASE_NAME

# Kết nối MongoDB
client = AsyncIOMotorClient(MONGO_URL)
database = client[DATABASE_NAME]


accounts_collection = database["accounts"]
