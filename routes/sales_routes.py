from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.sales_service import SalesService
from dependencies.auth_dependency import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()
sales_service = SalesService()

@router.post("/sales", dependencies=[Depends(get_current_user), Depends(limiter.limit("10/minute"))])
def create_sale(data: dict, db: Session = Depends(get_db)):
    try:
        new_sale = sales_service.create_sale(db, data)
        return {"message": "Sale created successfully", "sale": new_sale}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/sales/customer/{customer_id}", dependencies=[Depends(get_current_user), Depends(limiter.limit("10/minute"))])
def get_sales_by_customer(customer_id: int, db: Session = Depends(get_db)):
    return sales_service.get_sales_by_customer(db, customer_id)

@router.get("/sales/item/{item_id}", dependencies=[Depends(get_current_user), Depends(limiter.limit("10/minute"))])
def get_sales_by_item(item_id: int, db: Session = Depends(get_db)):
    return sales_service.get_sales_by_item(db, item_id)

@router.delete("/sales/{sale_id}", dependencies=[Depends(get_current_user), Depends(limiter.limit("10/minute"))])
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    try:
        sales_service.delete_sale(db, sale_id)
        return {"message": "Sale deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/sales/{sale_id}", dependencies=[Depends(get_current_user), Depends(limiter.limit("10/minute"))])
def update_sale(sale_id: int, updates: dict, db: Session = Depends(get_db)):
    try:
        updated_sale = sales_service.update_sale(db, sale_id, updates)
        return {"message": "Sale updated successfully", "sale": updated_sale}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
