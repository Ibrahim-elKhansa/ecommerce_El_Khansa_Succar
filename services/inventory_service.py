from sqlalchemy.orm import Session
from models.inventory import Item
from memory_profiler import profile

class InventoryService:
    @profile
    def create_item(self, db: Session, data: dict):
        if not data.get("name") or not data.get("stock_count"):
            raise ValueError("Name and stock count are required")
        
        new_item = Item(
            name=data["name"],
            category=data.get("category", ""),
            price=data.get("price", 0.0),
            description=data.get("description", ""),
            stock_count=data["stock_count"]
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

    @profile
    def update_item(self, db: Session, item_id: int, data: dict):
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise ValueError("Item not found")

        for key, value in data.items():
            setattr(item, key, value)

        db.commit()
        db.refresh(item)
        return item

    @profile
    def deduct_item(self, db: Session, item_id: int):
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise ValueError("Item not found")
        if item.stock_count <= 0:
            raise ValueError("No stock available to deduct")

        item.stock_count -= 1
        db.commit()
        db.refresh(item)
        return item

    @profile
    def get_all_items(self, db: Session):
        return db.query(Item).all()

    @profile
    def get_item_details(self, db: Session, item_id: int):
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise ValueError("Item not found")
        return item

    @profile
    def delete_all_items(self, db: Session):
        db.query(Item).delete()
        db.commit()
