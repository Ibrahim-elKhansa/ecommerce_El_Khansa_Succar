import os
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.sales_service import SalesService
from dependencies.auth_dependency import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

# Set up logging
os.makedirs("logs", exist_ok=True)  # Ensure logs directory exists
logging.basicConfig(
    filename="logs/log_sales.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()
sales_service = SalesService()

@router.post("/sales", dependencies=[Depends(get_current_user)])
def create_sale(data: dict, db: Session = Depends(get_db)):
    logging.info(f"POST /sales - Data: {data}")
    try:
        new_sale = sales_service.create_sale(db, data)
        logging.info(f"Sale created: {new_sale}")
        return {"message": "Sale created successfully", "sale": new_sale}
    except ValueError as e:
        logging.error(f"Error creating sale: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/sales/customer/{customer_id}", dependencies=[Depends(get_current_user)])
def get_sales_by_customer(customer_id: int, db: Session = Depends(get_db)):
    logging.info(f"GET /sales/customer/{customer_id}")
    sales = sales_service.get_sales_by_customer(db, customer_id)
    logging.info(f"Sales retrieved for customer_id={customer_id}: {len(sales)} sales")
    return sales

@router.get("/sales/item/{item_id}", dependencies=[Depends(get_current_user)])
def get_sales_by_item(item_id: int, db: Session = Depends(get_db)):
    logging.info(f"GET /sales/item/{item_id}")
    sales = sales_service.get_sales_by_item(db, item_id)
    logging.info(f"Sales retrieved for item_id={item_id}: {len(sales)} sales")
    return sales

@router.delete("/sales/{sale_id}", dependencies=[Depends(get_current_user)])
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    logging.info(f"DELETE /sales/{sale_id}")
    try:
        sales_service.delete_sale(db, sale_id)
        logging.info(f"Sale deleted: {sale_id}")
        return {"message": "Sale deleted successfully"}
    except ValueError as e:
        logging.error(f"Error deleting sale {sale_id}: {e}")
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/sales/{sale_id}", dependencies=[Depends(get_current_user)])
def update_sale(sale_id: int, updates: dict, db: Session = Depends(get_db)):
    logging.info(f"PUT /sales/{sale_id} - Updates: {updates}")
    try:
        updated_sale = sales_service.update_sale(db, sale_id, updates)
        logging.info(f"Sale updated: {updated_sale}")
        return {"message": "Sale updated successfully", "sale": updated_sale}
    except ValueError as e:
        logging.error(f"Error updating sale {sale_id}: {e}")
        raise HTTPException(status_code=404, detail=str(e))
