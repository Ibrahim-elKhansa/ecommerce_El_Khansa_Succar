from sqlalchemy.orm import Session
from models.sales import Sale
from sqlalchemy.exc import SQLAlchemyError

try:
    from line_profiler import profile
except ImportError:
    def profile(func):
        return func


class SalesService:
    def __init__(self):
        pass

    @profile
    def create_sale(self, db: Session, data: dict):
        try:
            sale = Sale(**data)
            db.add(sale)
            db.commit()
            db.refresh(sale)
            return sale
        except SQLAlchemyError as e:
            db.rollback()
            raise ValueError(f"Failed to create sale: {e}")

    @profile
    def get_sales_by_customer(self, db: Session, customer_id: int):
        try:
            return db.query(Sale).filter(Sale.customer_id == customer_id).all()
        except SQLAlchemyError as e:
            raise ValueError(f"Failed to retrieve sales for customer {customer_id}: {e}")

    @profile
    def get_sales_by_item(self, db: Session, item_id: int):
        try:
            return db.query(Sale).filter(Sale.item_id == item_id).all()
        except SQLAlchemyError as e:
            raise ValueError(f"Failed to retrieve sales for item {item_id}: {e}")

    @profile
    def delete_sale(self, db: Session, sale_id: int):
        try:
            sale = db.query(Sale).filter(Sale.id == sale_id).first()
            if not sale:
                raise ValueError("Sale not found")
            db.delete(sale)
            db.commit()
            return {"message": f"Sale {sale_id} successfully deleted"}
        except SQLAlchemyError as e:
            db.rollback()
            raise ValueError(f"Failed to delete sale {sale_id}: {e}")

    @profile
    def update_sale(self, db: Session, sale_id: int, updates: dict):
        try:
            sale = db.query(Sale).filter(Sale.id == sale_id).first()
            if not sale:
                raise ValueError("Sale not found")
            for key, value in updates.items():
                setattr(sale, key, value)
            db.commit()
            db.refresh(sale)
            return sale
        except SQLAlchemyError as e:
            db.rollback()
            raise ValueError(f"Failed to update sale {sale_id}: {e}")
