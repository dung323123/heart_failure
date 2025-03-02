from pymongo import ASCENDING
from app.database import database

# Khởi tạo collection items
items_collection = database["items"]
items_collection.create_index([("name", ASCENDING)], unique=True)
