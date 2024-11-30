from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.customer_service import CustomerService

router = APIRouter()
customer_service = CustomerService()  # Create an instance of the service

@router.post("/customers")
def create_customer_route(customer_data: dict, db: Session = Depends(get_db)):
    try:
        new_customer = customer_service.create_customer(db, customer_data)  # Use the instance method
        return {"message": "Customer created successfully", "customer": new_customer}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/customers/{username}")
def get_customer_by_username(username: str, db: Session = Depends(get_db)):
    customer = customer_service.get_customer_by_username(db, username)  # Use the instance method
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.get("/customers")
def get_all_customers_route(db: Session = Depends(get_db)):
    return customer_service.get_all_customers(db)  # Use the instance method

@router.put("/customers/{username}")
def update_customer_route(username: str, updates: dict, db: Session = Depends(get_db)):
    try:
        updated_customer = customer_service.update_customer(db, username, updates)  # Use the instance method
        return {"message": "Customer updated successfully", "customer": updated_customer}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/customers/{username}")
def delete_customer_route(username: str, db: Session = Depends(get_db)):
    try:
        customer_service.delete_customer(db, username)  # Use the instance method
        return {"message": "Customer deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/customers/{username}/charge")
def charge_wallet_route(username: str, amount: float, db: Session = Depends(get_db)):
    try:
        charged_customer = customer_service.charge_wallet(db, username, amount)  # Use the instance method
        return {"message": "Wallet charged successfully", "customer": charged_customer}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/customers/{username}/deduct")
def deduct_wallet_route(username: str, amount: float, db: Session = Depends(get_db)):
    try:
        deducted_customer = customer_service.deduct_wallet(db, username, amount)  # Use the instance method
        return {"message": "Wallet deducted successfully", "customer": deducted_customer}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
