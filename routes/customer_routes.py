from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.customer_service import CustomerService
from dependencies.auth_dependency import get_current_user

router = APIRouter()
customer_service = CustomerService()

@router.get("/customers", dependencies=[Depends(get_current_user)])
def get_all_customers(db: Session = Depends(get_db)):
    return customer_service.get_all_customers(db)

@router.get("/customers/{customer_id}", dependencies=[Depends(get_current_user)])
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = customer_service.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/customers", dependencies=[Depends(get_current_user)])
def create_customer(data: dict, db: Session = Depends(get_db)):
    try:
        new_customer = customer_service.create_customer(db, data)
        return {"message": "Customer created successfully", "customer": new_customer}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/customers/{customer_id}", dependencies=[Depends(get_current_user)])
def update_customer(customer_id: int, updates: dict, db: Session = Depends(get_db)):
    try:
        updated_customer = customer_service.update_customer(db, customer_id, updates)
        return {"message": "Customer updated successfully", "customer": updated_customer}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/customers/{customer_id}", dependencies=[Depends(get_current_user)])
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    try:
        customer_service.delete_customer(db, customer_id)
        return {"message": "Customer deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
