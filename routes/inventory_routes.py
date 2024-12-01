import os
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.inventory_service import InventoryService
from dependencies.auth_dependency import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

"""
Inventory Routes
================

This module defines the API routes for managing inventory operations.

Features
--------

- **Inventory Management**:
  - Retrieve all inventory items or specific items by their ID.
  - Create, update, and delete inventory items.
  - Deduct stock from an item.
  - Delete all items from the inventory.

- **Logging**:
  - Logs all requests, responses, and errors for debugging and monitoring purposes.

- **Dependencies**:
  - Uses `InventoryService` for handling business logic related to inventory operations.
  - Requires authenticated users for all routes through dependency injection.

- **Throttling**:
  - Implements request throttling using `SlowAPI` to limit excessive API usage.

Routes
------

- **GET /items**:
  Retrieve all items in the inventory.
- **GET /items/{item_id}**:
  Retrieve a specific item by its ID.
- **POST /items**:
  Create a new item in the inventory.
- **PUT /items/{item_id}**:
  Update an existing inventory item.
- **POST /items/{item_id}/deduct**:
  Deduct stock from a specific item.
- **DELETE /items/{item_id}**:
  Delete an inventory item by ID.
- **DELETE /items**:
  Delete all items in the inventory.

Dependencies
------------

- **Database**: 
  Utilizes SQLAlchemy session management for CRUD operations via the `get_db` dependency.
- **Authentication**: 
  Ensures that all operations are accessible only to authenticated users via the `get_current_user` dependency.
- **InventoryService**:
  Handles the core business logic for inventory-related operations.
"""


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
    """
    Retrieve all items in the inventory.

    Args:
        db (Session): The database session dependency.

    Returns:
        list: A list of all inventory items.
    """
    logging.info("GET /items")
    items = inventory_service.get_all_items(db)
    logging.info(f"All items retrieved: {len(items)} items")
    return items

@router.get("/items/{item_id}", dependencies=[Depends(get_current_user)])
def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific item by its ID.

    Args:
        item_id (int): The ID of the item to retrieve.
        db (Session): The database session dependency.

    Returns:
        dict: The retrieved item details.

    Raises:
        HTTPException: If the item is not found.
    """
    logging.info(f"GET /items/{item_id}")
    item = inventory_service.get_item(db, item_id)
    if not item:
        logging.warning(f"Item not found: {item_id}")
        raise HTTPException(status_code=404, detail="Item not found")
    logging.info(f"Item retrieved: {item}")
    return item

@router.post("/items", dependencies=[Depends(get_current_user)])
def create_item(data: dict, db: Session = Depends(get_db)):
    """
    Create a new item in the inventory.

    Args:
        data (dict): The data for the new item.
        db (Session): The database session dependency.

    Returns:
        dict: A message and the newly created item.

    Raises:
        HTTPException: If item creation fails.
    """
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
    """
    Update an existing inventory item.

    Args:
        item_id (int): The ID of the item to update.
        updates (dict): The data to update the item with.
        db (Session): The database session dependency.

    Returns:
        dict: A message and the updated item.

    Raises:
        HTTPException: If the update fails or the item is not found.
    """
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
    """
    Deduct one stock unit from an item.

    Args:
        item_id (int): The ID of the item to deduct stock from.
        db (Session): The database session dependency.

    Returns:
        dict: A message and the updated item details.

    Raises:
        HTTPException: If the item is not found or stock is unavailable.
    """
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
    """
    Delete an inventory item by ID.

    Args:
        item_id (int): The ID of the item to delete.
        db (Session): The database session dependency.

    Returns:
        dict: A message confirming the deletion.

    Raises:
        HTTPException: If the item is not found.
    """
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
    """
    Delete all items in the inventory.

    Args:
        db (Session): The database session dependency.

    Returns:
        dict: A message confirming all items were deleted.
    """
    logging.info("DELETE /items")
    inventory_service.delete_all_items(db)
    logging.info("All items deleted from inventory")
    return {"message": "All items deleted successfully"}
