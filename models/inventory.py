from sqlalchemy import Column, Integer, String, Float
from database import Base

class Item(Base):
    """
    SQLAlchemy model representing an item in the inventory.

    Attributes
    ----------
    id : int
        The primary key of the item.
    name : str
        The name of the item.
    category : str
        The category to which the item belongs.
    price : float
        The price of the item.
    description : str, optional
        A brief description of the item.
    stock_count : int
        The number of items available in stock.
    """
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String)
    stock_count = Column(Integer, nullable=False)