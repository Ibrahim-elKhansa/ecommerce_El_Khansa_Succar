from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.inventory import Item
from services.inventory_service import InventoryService
from database import get_db

router = APIRouter()
inventory_service = InventoryService()

@router.post("/inventory")
def add_item(item_data: dict, db: Session = Depends(get_db)):
    try:
        new_item = inventory_service.create_item(db, item_data)
        return {"message": "Item added successfully", "item": new_item}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/inventory/{item_id}")
def update_item(item_id: int, updates: dict, db: Session = Depends(get_db)):
    try:
        updated_item = inventory_service.update_item(db, item_id, updates)
        return {"message": "Item updated successfully", "item": updated_item}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/inventory/{item_id}/deduct")
def deduct_item(item_id: int, db: Session = Depends(get_db)):
    try:
        inventory_service.deduct_item(db, item_id)
        return {"message": "Item deducted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/inventory")
def list_items(db: Session = Depends(get_db)):
    items = inventory_service.get_all_items(db)
    return items

@router.get("/inventory/{item_id}")
def get_item_details(item_id: int, db: Session = Depends(get_db)):
    try:
        item = inventory_service.get_item_details(db, item_id)
        return item
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
