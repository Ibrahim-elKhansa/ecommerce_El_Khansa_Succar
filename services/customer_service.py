from sqlalchemy.orm import Session
from models.customer import Customer
from memory_profiler import profile  # Import for memory profiling

@profile
def create_customer(db: Session, customer_data: dict):
    new_customer = Customer(**customer_data)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@profile
def get_customer_by_username(db: Session, username: str):
    return db.query(Customer).filter(Customer.username == username).first()

@profile
def get_all_customers(db: Session):
    return db.query(Customer).all()

@profile
def update_customer(db: Session, username: str, updates: dict):
    customer = get_customer_by_username(db, username)
    if customer:
        for key, value in updates.items():
            setattr(customer, key, value)
        db.commit()
        db.refresh(customer)
    return customer

@profile
def delete_customer(db: Session, username: str):
    customer = get_customer_by_username(db, username)
    if customer:
        db.delete(customer)
        db.commit()
    return customer

@profile
def charge_wallet(db: Session, username: str, amount: float):
    customer = get_customer_by_username(db, username)
    if customer:
        customer.wallet_balance += amount
        db.commit()
        db.refresh(customer)
    return customer

@profile
def deduct_wallet(db: Session, username: str, amount: float):
    customer = get_customer_by_username(db, username)
    if customer and customer.wallet_balance >= amount:
        customer.wallet_balance -= amount
        db.commit()
        db.refresh(customer)
    return customer
if __name__ == "__main__":
    from database import SessionLocal

    # Create a database session
    db = SessionLocal()

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
    created_customer = create_customer(db, sample_customer)
    print(f"Created customer: {created_customer}")

    # Retrieve customer by username
    print("Fetching customer by username...")
    fetched_customer = get_customer_by_username(db, "johndoe")
    print(f"Fetched customer: {fetched_customer}")

    # Retrieve all customers
    print("Fetching all customers...")
    all_customers = get_all_customers(db)
    print(f"All customers: {all_customers}")

    # Update customer
    print("Updating customer...")
    updated_customer = update_customer(db, "johndoe", {"address": "456 Elm Street", "wallet_balance": 150.0})
    print(f"Updated customer: {updated_customer}")

    # Charge wallet
    print("Charging wallet...")
    charged_customer = charge_wallet(db, "johndoe", 50.0)
    print(f"Charged wallet: {charged_customer}")

    # Deduct wallet
    print("Deducting wallet...")
    deducted_customer = deduct_wallet(db, "johndoe", 20.0)
    print(f"Deducted wallet: {deducted_customer}")

    # Delete customer
    print("Deleting customer...")
    delete_customer(db, "johndoe")
    print("Customer deleted.")

    db.close()
