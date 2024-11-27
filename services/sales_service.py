from sqlalchemy.orm import Session
from models.sales import Item, Customer, Sale

class SalesService:
    def display_goods(self, db: Session):
        """
        Retrieve all available goods with their names and prices.
        """
        return db.query(Item.name, Item.price).all()

    def get_good_details(self, db: Session, item_id: int):
        """
        Retrieve full details of a specific item by ID.
        """
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise ValueError("Item not found")
        return {
            "id": item.id,
            "name": item.name,
            "category": item.category,
            "price": item.price,
            "description": item.description,
            "stock_count": item.stock_count,
        }

    def process_sale(self, db: Session, username: str, item_id: int):
        """
        Process a sale:
        - Deduct stock from the item.
        - Deduct the price from the customer's wallet balance.
        - Create a new sale record.
        """
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise ValueError("Item not found")

        if item.stock_count <= 0:
            raise ValueError("Item is out of stock")

        customer = db.query(Customer).filter(Customer.username == username).first()
        if not customer:
            raise ValueError("Customer not found")

        if customer.wallet_balance < item.price:
            raise ValueError("Insufficient funds")

        item.stock_count -= 1
        customer.wallet_balance -= item.price

        new_sale = Sale(
            customer_id=customer.id,
            item_id=item.id,
            amount=item.price,
        )
        db.add(new_sale)

        db.commit()
        db.refresh(new_sale)

        return {
            "sale_id": new_sale.id,
            "customer_username": customer.username,
            "item_name": item.name,
            "amount": new_sale.amount,
        }
