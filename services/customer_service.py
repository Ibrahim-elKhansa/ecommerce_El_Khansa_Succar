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
