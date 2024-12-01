import os
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.inventory_service import InventoryService
from dependencies.auth_dependency import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

# Set up logging
os.makedirs("logs", exist_ok=True)  # Ensure logs directory exists
logging.basicConfig(
    filename="logs/log_inventory.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

router = APIRouter()
inventory_service = InventoryService()
limiter = Limiter(key_func=get_remote_address)

@router.get("/items", dependencies=[Depends(get_current_user)])
def get_all_items(db: Session = Depends(get_db)):
    logging.info("GET /items")
    items = inventory_service.get_all_items(db)
    logging.info(f"All items retrieved: {len(items)} items")
    return items

@router.get("/items/{item_id}", dependencies=[Depends(get_current_user)])
def get_item(item_id: int, db: Session = Depends(get_db)):
    logging.info(f"GET /items/{item_id}")
    item = inventory_service.get_item(db, item_id)
    if not item:
        logging.warning(f"Item not found: {item_id}")
        raise HTTPException(status_code=404, detail="Item not found")
    logging.info(f"Item retrieved: {item}")
    return item

@router.post("/items", dependencies=[Depends(get_current_user)])
def create_item(data: dict, db: Session = Depends(get_db)):
    logging.info(f"POST /items - Data: {data}")
    try:
        new_item = inventory_service.create_item(db, data)
        logging.info(f"Item created: {new_item}")
        return {"message": "Item created successfully", "item": new_item}
    except ValueError as e:
        logging.error(f"Error creating item: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/items/{item_id}", dependencies=[Depends(get_current_user)])
def update_item(item_id: int, updates: dict, db: Session = Depends(get_db)):
    logging.info(f"PUT /items/{item_id} - Updates: {updates}")
    try:
        updated_item = inventory_service.update_item(db, item_id, updates)
        logging.info(f"Item updated: {updated_item}")
        return {"message": "Item updated successfully", "item": updated_item}
    except ValueError as e:
        logging.error(f"Error updating item {item_id}: {e}")
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/items/{item_id}/deduct", dependencies=[Depends(get_current_user)])
def deduct_item(item_id: int, db: Session = Depends(get_db)):
    logging.info(f"POST /items/{item_id}/deduct")
    try:
        updated_item = inventory_service.deduct_item(db, item_id)
        logging.info(f"Item stock deducted: {updated_item}")
        return {"message": "Item deducted successfully", "item": updated_item}
    except ValueError as e:
        if str(e) == "No stock available to deduct":
            logging.warning(f"Stock deduction failed for item {item_id}: No stock available")
            raise HTTPException(status_code=400, detail=str(e))
        logging.error(f"Error deducting item {item_id}: {e}")
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/items/{item_id}", dependencies=[Depends(get_current_user)])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    logging.info(f"DELETE /items/{item_id}")
    try:
        inventory_service.delete_item(db, item_id)
        logging.info(f"Item deleted: {item_id}")
        return {"message": "Item deleted successfully"}
    except ValueError as e:
        logging.error(f"Error deleting item {item_id}: {e}")
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/items", dependencies=[Depends(get_current_user)])
def delete_all_items(db: Session = Depends(get_db)):
    logging.info("DELETE /items")
    inventory_service.delete_all_items(db)
    logging.info("All items deleted from inventory")
    return {"message": "All items deleted successfully"}
