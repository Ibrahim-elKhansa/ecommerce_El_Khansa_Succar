from sqlalchemy import Column, Integer, Float
from database import Base

class Sale(Base):
    """
    SQLAlchemy model representing a sales record.

    Attributes
    ----------
    id : int
        The primary key of the sale record.
    customer_id : int
        The ID of the customer associated with the sale.
    item_id : int
        The ID of the item being sold.
    amount : float
        The monetary amount of the sale.
    """
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, nullable=False)
    item_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
