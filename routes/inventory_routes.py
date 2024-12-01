from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.inventory_service import InventoryService
from dependencies.auth_dependency import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
inventory_service = InventoryService()
limiter = Limiter(key_func=get_remote_address)

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

@router.post("/items/{item_id}/deduct", dependencies=[Depends(get_current_user)])
def deduct_item(item_id: int, db: Session = Depends(get_db)):
    try:
        updated_item = inventory_service.deduct_item(db, item_id)
        return {"message": "Item deducted successfully", "item": updated_item}
    except ValueError as e:
        if str(e) == "No stock available to deduct":
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/items/{item_id}", dependencies=[Depends(get_current_user)])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    try:
        inventory_service.delete_item(db, item_id)
        return {"message": "Item deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/items", dependencies=[Depends(get_current_user)])
def delete_all_items(db: Session = Depends(get_db)):
    """
    Delete all items in the inventory.
    """
    inventory_service.delete_all_items(db)
    return {"message": "All items deleted successfully"}
