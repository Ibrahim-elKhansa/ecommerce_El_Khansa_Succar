from sqlalchemy.orm import Session
from models.sales import Sale
from sqlalchemy.exc import SQLAlchemyError
from memory_profiler import profile
import time
import pybreaker
import requests

circuit_breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=30)
try:
    from line_profiler import profile
except ImportError:
    def profile(func):
        return func



class SalesService:
    """
    A service class for managing sales, including operations to create, retrieve, update, and delete sales.

    Methods:
        call_sales_api(endpoint: str, data: dict): Calls an external sales API.
        create_sale(db: Session, data: dict): Creates a new sale record in the database.
        get_sales_by_customer(db: Session, customer_id: int): Retrieves all sales associated with a specific customer.
        get_sales_by_item(db: Session, item_id: int): Retrieves all sales associated with a specific item.
        delete_sale(db: Session, sale_id: int): Deletes a sale record by its ID.
        update_sale(db: Session, sale_id: int, updates: dict): Updates an existing sale record with new data.
    """
    @circuit_breaker
    def call_sales_api(self, endpoint: str, data: dict):
        """
        Calls an external sales API.

        Args:
            endpoint (str): The API endpoint URL.
            data (dict): The data payload to send with the request.

        Returns:
            dict: The JSON response from the API.

        Raises:
            Exception: If the API call fails.
        """
        try:
            response = requests.post(f"http://127.0.0.1:8002/api/", json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to call sales API: {e}")
    def __init__(self):
        pass

    @profile
    def create_sale(self, db: Session, data: dict):
        """
        Creates a new sale record in the database.

        Args:
            db (Session): The database session.
            data (dict): The sale data to create.

        Returns:
            Sale: The created sale record.

        Raises:
            ValueError: If the sale creation fails.
        """
        try:
            sale = Sale(**data)
            db.add(sale)
            db.commit()
            db.refresh(sale)
            return sale
        except SQLAlchemyError as e:
            db.rollback()
            raise ValueError(f"Failed to create sale: {e}")

    @profile
    def get_sales_by_customer(self, db: Session, customer_id: int):
        """
        Retrieves all sales associated with a specific customer.

        Args:
            db (Session): The database session.
            customer_id (int): The ID of the customer.

        Returns:
            list[Sale]: A list of sales associated with the customer.

        Raises:
            ValueError: If the query fails.
        """
        try:
            return db.query(Sale).filter(Sale.customer_id == customer_id).all()
        except SQLAlchemyError as e:
            raise ValueError(f"Failed to retrieve sales for customer {customer_id}: {e}")

    @profile
    def get_sales_by_item(self, db: Session, item_id: int):
        """
        Retrieves all sales associated with a specific item.

        Args:
            db (Session): The database session.
            item_id (int): The ID of the item.

        Returns:
            list[Sale]: A list of sales associated with the item.

        Raises:
            ValueError: If the query fails.
        """
        try:
            return db.query(Sale).filter(Sale.item_id == item_id).all()
        except SQLAlchemyError as e:
            raise ValueError(f"Failed to retrieve sales for item {item_id}: {e}")

    @profile
    def delete_sale(self, db: Session, sale_id: int):
        """
        Deletes a sale record by its ID.

        Args:
            db (Session): The database session.
            sale_id (int): The ID of the sale to delete.

        Returns:
            dict: A success message indicating the sale was deleted.

        Raises:
            ValueError: If the sale is not found or deletion fails.
        """
        try:
            sale = db.query(Sale).filter(Sale.id == sale_id).first()
            if not sale:
                raise ValueError("Sale not found")
            db.delete(sale)
            db.commit()
            return {"message": f"Sale {sale_id} successfully deleted"}
        except SQLAlchemyError as e:
            db.rollback()
            raise ValueError(f"Failed to delete sale {sale_id}: {e}")

    @profile
    def update_sale(self, db: Session, sale_id: int, updates: dict):
        """
        Updates an existing sale record with new data.

        Args:
            db (Session): The database session.
            sale_id (int): The ID of the sale to update.
            updates (dict): A dictionary of updates for the sale.

        Returns:
            Sale: The updated sale record.

        Raises:
            ValueError: If the sale is not found or update fails.
        """
        try:
            sale = db.query(Sale).filter(Sale.id == sale_id).first()
            if not sale:
                raise ValueError("Sale not found")
            for key, value in updates.items():
                setattr(sale, key, value)
            db.commit()
            db.refresh(sale)
            return sale
        except SQLAlchemyError as e:
            db.rollback()
            raise ValueError(f"Failed to update sale {sale_id}: {e}")
if __name__ == "__main__":
    from database import SessionLocal

    # Create a database session
    db = SessionLocal()
    service = SalesService()

    # Sample data for testing
    sample_sale = {
        "customer_id": 1,
        "item_id": 2,
        "amount": 100.0
    }

    # Test create_sale
    print("Creating a sale...")
    created_sale = service.create_sale(db, sample_sale)
    print(f"Created sale ID: {created_sale.id}")

    # Test get_sales_by_customer
    print(f"Fetching sales for customer ID {sample_sale['customer_id']}...")
    customer_sales = service.get_sales_by_customer(db, sample_sale["customer_id"])
    print(f"Sales for customer ID {sample_sale['customer_id']}: {customer_sales}")

    # Test get_sales_by_item
    print(f"Fetching sales for item ID {sample_sale['item_id']}...")
    item_sales = service.get_sales_by_item(db, sample_sale["item_id"])
    print(f"Sales for item ID {sample_sale['item_id']}: {item_sales}")

    # Test update_sale
    print(f"Updating sale ID {created_sale.id}...")
    updated_sale = service.update_sale(
        db,
        created_sale.id,
        {"amount": 150.0}
    )
    print(f"Updated sale: {updated_sale}")

    # Test delete_sale
    print(f"Deleting sale ID {created_sale.id}...")
    delete_response = service.delete_sale(db, created_sale.id)
    print(delete_response)

    db.close()
    time.sleep(5)
