from fastapi import FastAPI, HTTPException
from models import Item
from database import collection
from bson import ObjectId
from typing import List

app = FastAPI()

# Helper function to format MongoDB documents
def item_helper(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "description": item["description"],
        "price": item["price"],
        "tax": item["tax"],
    }

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    new_item = collection.insert_one(item.dict())
    created_item = collection.find_one({"_id": new_item.inserted_id})
    return item_helper(created_item)

@app.get("/items/", response_model=List[Item])
async def read_items():
    items = []
    for item in collection.find():
        items.append(item_helper(item))
    return items

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    if (item := collection.find_one({"_id": ObjectId(item_id)})) is not None:
        return item_helper(item)
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    updated_item = collection.find_one_and_update(
        {"_id": ObjectId(item_id)},
        {"$set": item.dict()},
        return_document=True
    )
    if updated_item:
        return item_helper(updated_item)
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    delete_result = collection.delete_one({"_id": ObjectId(item_id)})
    if delete_result.deleted_count == 1:
        return {"detail": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
