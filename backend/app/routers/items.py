from fastapi import APIRouter, HTTPException
from app.models import items_collection
from app.schemas import Item
from bson import ObjectId

router = APIRouter()

@router.post("/items/")
async def create_item(item: Item):
    if await items_collection.find_one({"name": item.name}):
        raise HTTPException(status_code=400, detail="Item already exists")
    result = await items_collection.insert_one(item.dict())
    return {"id": str(result.inserted_id)}

@router.get("/items/")
async def get_items():
    items = await items_collection.find().to_list(100)
    return [{"id": str(item["_id"]), "name": item["name"], "description": item.get("description", "")} for item in items]
