from sqlalchemy.orm import Session
from models.inventory import Item
from memory_profiler import profile
from database import SessionLocal
import pybreaker
import requests

circuit_breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=30)


class InventoryService:
    """
    A service class for managing inventory operations.

    Methods:
        call_inventory_api(): Calls an external inventory API.
        create_item(): Creates a new inventory item.
        get_item(): Retrieves an item by its ID.
        update_item(): Updates an inventory item.
        deduct_item(): Deducts one unit from an item's stock count.
        get_all_items(): Retrieves all inventory items.
        get_item_details(): Retrieves detailed information about an item.
        delete_item(): Deletes a specific inventory item.
        delete_all_items(): Deletes all inventory items.
    """
    @circuit_breaker
    def call_inventory_api(self, endpoint: str, data: dict):
        """
        Calls an external inventory API.

        Args:
            endpoint (str): The API endpoint to call.
            data (dict): The data payload to send in the API request.

        Returns:
            dict: The response data from the API.

        Raises:
            Exception: If the API call fails.
        """
        try:
            response = requests.post(f"http://127.0.0.1:8001/api/", json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to call inventory API: {e}")
    @profile
    def create_item(self, db: Session, data: dict):
        """
        Creates a new inventory item.

        Args:
            db (Session): The database session.
            data (dict): A dictionary containing the item data.

        Returns:
            Item: The created inventory item.

        Raises:
            ValueError: If required fields are missing.
        """
        if not data.get("name") or not data.get("stock_count"):
            raise ValueError("Name and stock count are required")
        
        new_item = Item(
            name=data["name"],
            category=data.get("category", ""),
            price=data.get("price", 0.0),
            description=data.get("description", ""),
            stock_count=data["stock_count"]
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    
    @profile
    def get_item(self, db: Session, item_id: int):
        """
        Retrieves an item by its ID.

        Args:
            db (Session): The database session.
            item_id (int): The ID of the item.

        Returns:
            Item or None: The inventory item if found, else None.
        """
        return db.query(Item).filter(Item.id == item_id).first()

    @profile
    def update_item(self, db: Session, item_id: int, data: dict):
        """
        Updates an inventory item.

        Args:
            db (Session): The database session.
            item_id (int): The ID of the item to update.
            data (dict): The updated data for the item.

        Returns:
            Item: The updated inventory item.

        Raises:
            ValueError: If the item is not found.
        """
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise ValueError("Item not found")

        for key, value in data.items():
            setattr(item, key, value)

        db.commit()
        db.refresh(item)
        return item

    @profile
    def deduct_item(self, db: Session, item_id: int):
        """
        Deducts one unit from an item's stock count.

        Args:
            db (Session): The database session.
            item_id (int): The ID of the item to deduct.

        Returns:
            Item: The updated inventory item.

        Raises:
            ValueError: If the item is not found or has no stock available.
        """
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise ValueError("Item not found")
        if item.stock_count <= 0:
            raise ValueError("No stock available to deduct")

        item.stock_count -= 1
        db.commit()
        db.refresh(item)
        return item

    @profile
    def get_all_items(self, db: Session):
        """
        Retrieves all inventory items.

        Args:
            db (Session): The database session.

        Returns:
            list[Item]: A list of all inventory items.
        """
        return db.query(Item).all()

    @profile
    def get_item_details(self, db: Session, item_id: int):
        """
        Retrieves detailed information about an item.

        Args:
            db (Session): The database session.
            item_id (int): The ID of the item.

        Returns:
            Item: The inventory item if found.

        Raises:
            ValueError: If the item is not found.
        """
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise ValueError("Item not found")
        return item
    
    @profile
    def delete_item(self, db: Session, item_id: int):
        """
        Deletes a specific inventory item by its ID.

        Args:
            db (Session): The database session.
            item_id (int): The ID of the item to delete.

        Returns:
            dict: A success message.

        Raises:
            ValueError: If the item is not found.
        """
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise ValueError("Item not found")
        db.delete(item)
        db.commit()
        return {"message": f"Item with ID {item_id} deleted successfully"}

    @profile
    def delete_all_items(self, db: Session):
        """
        Deletes all inventory items.

        Args:
            db (Session): The database session.

        Returns:
            None
        """
        db.query(Item).delete()
        db.commit()


if __name__ == "__main__":
    # Create a database session
    db = SessionLocal()
    service = InventoryService()

    # Sample data for testing
    sample_item = {
        "name": "Test Item",
        "category": "Test Category",
        "price": 10.0,
        "description": "Sample description",
        "stock_count": 5
    }

    # Test create_item
    print("Creating an item...")
    created_item = service.create_item(db, sample_item)

    # Test get_all_items
    print("Fetching all items...")
    all_items = service.get_all_items(db)

    # Test get_item_details
    print(f"Fetching details of item ID {created_item.id}...")
    item_details = service.get_item_details(db, created_item.id)

    # Test update_item
    print(f"Updating item ID {created_item.id}...")
    updated_item = service.update_item(
        db,
        created_item.id,
        {"name": "Updated Item", "price": 15.0}
    )

    # Test deduct_item
    print(f"Deducting stock from item ID {created_item.id}...")
    deducted_item = service.deduct_item(db, created_item.id)

    # Test delete_all_items
    print("Deleting all items...")
    service.delete_all_items(db)