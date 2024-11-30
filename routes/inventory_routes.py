from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.inventory_service import InventoryService
from dependencies.auth_dependency import get_current_user

router = APIRouter()
inventory_service = InventoryService()

@router.get("/items", dependencies=[Depends(get_current_user)])
def get_all_items(db: Session = Depends(get_db)):
    return inventory_service.get_all_items(db)

@router.get("/items/{item_id}", dependencies=[Depends(get_current_user)])
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = inventory_service.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/items", dependencies=[Depends(get_current_user)])
def create_item(data: dict, db: Session = Depends(get_db)):
    try:
        new_item = inventory_service.create_item(db, data)
        return {"message": "Item created successfully", "item": new_item}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/items/{item_id}", dependencies=[Depends(get_current_user)])
def update_item(item_id: int, updates: dict, db: Session = Depends(get_db)):
    try:
        updated_item = inventory_service.update_item(db, item_id, updates)
        return {"message": "Item updated successfully", "item": updated_item}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/items/{item_id}", dependencies=[Depends(get_current_user)])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    try:
        inventory_service.delete_item(db, item_id)
        return {"message": "Item deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
