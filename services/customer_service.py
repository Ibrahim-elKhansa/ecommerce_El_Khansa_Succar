from sqlalchemy.orm import Session
from models.customer import Customer
from memory_profiler import profile
import pybreaker
import requests

circuit_breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=30)

class CustomerService:
    """
    A service class for managing customer-related operations.

    Methods:
        call_customer_api(): Makes an API call to the customer API.
        create_customer(): Creates a new customer in the database.
        get_customer_by_username(): Retrieves a customer by their username.
        get_all_customers(): Retrieves all customers from the database.
        update_customer(): Updates customer details in the database.
        delete_customer(): Deletes a customer from the database.
        charge_wallet(): Charges a customer's wallet with a specified amount.
        deduct_wallet(): Deducts a specified amount from a customer's wallet.
    """
    @circuit_breaker
    def call_customer_api(self, endpoint: str, data: dict):
        """
        Makes an API call to the customer API.

        Args:
            endpoint (str): The API endpoint to call.
            data (dict): The payload to send in the API request.

        Returns:
            dict: The API response data.

        Raises:
            Exception: If the API call fails.
        """
        try:
            response = requests.post(f"http://127.0.0.1:8000/api/", json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to call customer API: {e}")
    @profile
    def create_customer(self, db: Session, customer_data: dict):
        """
        Creates a new customer in the database.

        Args:
            db (Session): The database session.
            customer_data (dict): The customer data to create.

        Returns:
            Customer: The newly created customer.
        """
        new_customer = Customer(**customer_data)
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        return new_customer

    @profile
    def get_customer_by_username(self, db: Session, username: str):
        """
        Retrieves a customer by their username.

        Args:
            username (str): The username of the customer to retrieve.

        Returns:
            Customer or None: The customer if found, else None.
        """
        return db.query(Customer).filter(Customer.username == username).first()

    @profile
    def get_all_customers(self, db: Session):
        """
        Retrieves all customers from the database.

        Args:
            db (Session): The database session.

        Returns:
            list[Customer]: A list of all customers.
        """
        return db.query(Customer).all()

    @profile
    def update_customer(self, db: Session, username: str, updates: dict):
        """
        Updates customer details in the database.

        Args:
            db (Session): The database session.
            username (str): The username of the customer to update.
            updates (dict): A dictionary of fields to update.

        Returns:
            Customer or None: The updated customer if found, else None.
        """
        customer = self.get_customer_by_username(db, username)
        if customer:
            for key, value in updates.items():
                setattr(customer, key, value)
            db.commit()
            db.refresh(customer)
        return customer

    @profile
    def delete_customer(self, db: Session, username: str):
        """
        Deletes a customer from the database.

        Args:
            db (Session): The database session.
            username (str): The username of the customer to delete.

        Returns:
            Customer or None: The deleted customer if found, else None.
        """
        customer = self.get_customer_by_username(db, username)
        if customer:
            db.delete(customer)
            db.commit()
        return customer

    @profile
    def charge_wallet(self, db: Session, username: str, amount: float):
        """
        Charges a customer's wallet with a specified amount.

        Args:
            db (Session): The database session.
            username (str): The username of the customer.
            amount (float): The amount to charge.

        Returns:
            Customer or None: The updated customer if found, else None.
        """
        customer = self.get_customer_by_username(db, username)
        if customer:
            customer.wallet_balance += amount
            db.commit()
            db.refresh(customer)
        return customer

    @profile
    def deduct_wallet(self, db: Session, username: str, amount: float):
        """
        Deducts a specified amount from a customer's wallet.

        Args:
            db (Session): The database session.
            username (str): The username of the customer.
            amount (float): The amount to deduct.

        Returns:
            Customer or None: The updated customer if found, else None.
        """
        customer = self.get_customer_by_username(db, username)
        if customer and customer.wallet_balance >= amount:
            customer.wallet_balance -= amount
            db.commit()
            db.refresh(customer)
        return customer

if __name__ == "__main__":
    from database import SessionLocal

    db = SessionLocal()
    service = CustomerService()

    sample_customer = {
        "full_name": "John Doe",
        "username": "johndoe",
        "password": "securepassword",
        "age": 30,  # Mandatory field
        "address": "123 Main Street",  # Mandatory field
        "gender": "Male",  # Mandatory field
        "marital_status": "Single",  # Mandatory field
        "wallet_balance": 100.0  # Optional field
    }

    # Create customer
    print("Creating a customer...")
    created_customer = service.create_customer(db, sample_customer)
    print(f"Created customer: {created_customer}")

    # Retrieve customer by username
    print("Fetching customer by username...")
    fetched_customer = service.get_customer_by_username(db, "johndoe")
    print(f"Fetched customer: {fetched_customer}")

    # Retrieve all customers
    print("Fetching all customers...")
    all_customers = service.get_all_customers(db)
    print(f"All customers: {all_customers}")

    # Update customer
    print("Updating customer...")
    updated_customer = service.update_customer(db, "johndoe", {"address": "456 Elm Street", "wallet_balance": 150.0})
    print(f"Updated customer: {updated_customer}")

    # Charge wallet
    print("Charging wallet...")
    charged_customer = service.charge_wallet(db, "johndoe", 50.0)
    print(f"Charged wallet: {charged_customer}")

    # Deduct wallet
    print("Deducting wallet...")
    deducted_customer = service.deduct_wallet(db, "johndoe", 20.0)
    print(f"Deducted wallet: {deducted_customer}")

    # Delete customer
    print("Deleting customer...")
    service.delete_customer(db, "johndoe")
    print("Customer deleted.")

    db.close()
