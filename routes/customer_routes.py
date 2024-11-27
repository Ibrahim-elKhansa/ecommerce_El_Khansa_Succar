from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.customer_service import (
    create_customer, get_customer_by_username, get_all_customers, 
    update_customer, delete_customer, charge_wallet, deduct_wallet
)

router = APIRouter()

@router.post("/customers")
def register_customer(customer_data: dict, db: Session = Depends(get_db)):
    if get_customer_by_username(db, customer_data["username"]):
        raise HTTPException(status_code=400, detail="Username already taken")
    return create_customer(db, customer_data)

@router.get("/customers")
def list_customers(db: Session = Depends(get_db)):
    return get_all_customers(db)

@router.get("/customers/{username}")
def get_customer(username: str, db: Session = Depends(get_db)):
    customer = get_customer_by_username(db, username)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/customers/{username}")
def update_customer_info(username: str, updates: dict, db: Session = Depends(get_db)):
    customer = update_customer(db, username, updates)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.delete("/customers/{username}")
def remove_customer(username: str, db: Session = Depends(get_db)):
    customer = delete_customer(db, username)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}

@router.post("/customers/{username}/charge")
def charge_customer(username: str, amount: float, db: Session = Depends(get_db)):
    customer = charge_wallet(db, username, amount)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/customers/{username}/deduct")
def deduct_customer(username: str, amount: float, db: Session = Depends(get_db)):
    customer = deduct_wallet(db, username, amount)
    if not customer:
        raise HTTPException(status_code=400, detail="Insufficient funds or customer not found")
    return customer
