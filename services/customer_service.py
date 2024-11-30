from sqlalchemy.orm import Session
from models.customer import Customer
from memory_profiler import profile  # Import for memory profiling

class CustomerService:
    @profile
    def create_customer(self, db: Session, customer_data: dict):
        new_customer = Customer(**customer_data)
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        return new_customer
class CustomerService:
    @profile
    def create_customer(self, db: Session, customer_data: dict):
        new_customer = Customer(**customer_data)
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        return new_customer

    @profile
    def get_customer_by_username(self, db: Session, username: str):
        return db.query(Customer).filter(Customer.username == username).first()
    @profile
    def get_customer_by_username(self, db: Session, username: str):
        return db.query(Customer).filter(Customer.username == username).first()

    @profile
    def get_all_customers(self, db: Session):
        return db.query(Customer).all()
    @profile
    def get_all_customers(self, db: Session):
        return db.query(Customer).all()

    @profile
    def update_customer(self, db: Session, username: str, updates: dict):
        customer = self.get_customer_by_username(db, username)  # Fixed reference to class method
        if customer:
            for key, value in updates.items():
                setattr(customer, key, value)
            db.commit()
            db.refresh(customer)
        return customer
    @profile
    def update_customer(self, db: Session, username: str, updates: dict):
        customer = self.get_customer_by_username(db, username)  # Fixed reference to class method
        if customer:
            for key, value in updates.items():
                setattr(customer, key, value)
            db.commit()
            db.refresh(customer)
        return customer

    @profile
    def delete_customer(self, db: Session, username: str):
        customer = self.get_customer_by_username(db, username)  # Fixed reference to class method
        if customer:
            db.delete(customer)
            db.commit()
        return customer
    @profile
    def delete_customer(self, db: Session, username: str):
        customer = self.get_customer_by_username(db, username)  # Fixed reference to class method
        if customer:
            db.delete(customer)
            db.commit()
        return customer

    @profile
    def charge_wallet(self, db: Session, username: str, amount: float):
        customer = self.get_customer_by_username(db, username)  # Fixed reference to class method
        if customer:
            customer.wallet_balance += amount
            db.commit()
            db.refresh(customer)
        return customer
    @profile
    def charge_wallet(self, db: Session, username: str, amount: float):
        customer = self.get_customer_by_username(db, username)  # Fixed reference to class method
        if customer:
            customer.wallet_balance += amount
            db.commit()
            db.refresh(customer)
        return customer

    @profile
    def deduct_wallet(self, db: Session, username: str, amount: float):
        customer = self.get_customer_by_username(db, username)  # Fixed reference to class method
        if customer and customer.wallet_balance >= amount:
            customer.wallet_balance -= amount
            db.commit()
            db.refresh(customer)
        return customer

if __name__ == "_main_":
    from database import SessionLocal

    # Create a database session
    db = SessionLocal()
    service = CustomerService()
    service = CustomerService()

    # Sample data for testing
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
    created_customer = service.create_customer(db, sample_customer)
    print(f"Created customer: {created_customer}")

    # Retrieve customer by username
    print("Fetching customer by username...")
    fetched_customer = service.get_customer_by_username(db, "johndoe")
    fetched_customer = service.get_customer_by_username(db, "johndoe")
    print(f"Fetched customer: {fetched_customer}")

    # Retrieve all customers
    print("Fetching all customers...")
    all_customers = service.get_all_customers(db)
    all_customers = service.get_all_customers(db)
    print(f"All customers: {all_customers}")

    # Update customer
    print("Updating customer...")
    updated_customer = service.update_customer(db, "johndoe", {"address": "456 Elm Street", "wallet_balance": 150.0})
    updated_customer = service.update_customer(db, "johndoe", {"address": "456 Elm Street", "wallet_balance": 150.0})
    print(f"Updated customer: {updated_customer}")

    # Charge wallet
    print("Charging wallet...")
    charged_customer = service.charge_wallet(db, "johndoe", 50.0)
    charged_customer = service.charge_wallet(db, "johndoe", 50.0)
    print(f"Charged wallet: {charged_customer}")

    # Deduct wallet
    print("Deducting wallet...")
    deducted_customer = service.deduct_wallet(db, "johndoe", 20.0)
    deducted_customer = service.deduct_wallet(db, "johndoe", 20.0)
    print(f"Deducted wallet: {deducted_customer}")

    # Delete customer
    print("Deleting customer...")
    service.delete_customer(db, "johndoe")
    service.delete_customer(db, "johndoe")
    print("Customer deleted.")

    db.close()