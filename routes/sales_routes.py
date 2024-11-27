from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.sales import Item, Sale, Customer
from services.sales_service import SalesService

router = APIRouter()
sales_service = SalesService()

@router.get("/sales/goods")
def display_goods(db: Session = Depends(get_db)):
    return sales_service.display_goods(db)

@router.get("/sales/goods/{item_id}")
def get_good_details(item_id: int, db: Session = Depends(get_db)):
    try:
        return sales_service.get_good_details(db, item_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/sales/{username}")
def process_sale(username: str, item_id: int, db: Session = Depends(get_db)):
    try:
        return sales_service.process_sale(db, username, item_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
