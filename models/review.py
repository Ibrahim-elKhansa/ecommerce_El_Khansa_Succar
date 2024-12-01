from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Review(Base):
    """
    SQLAlchemy model representing customer reviews.

    Attributes
    ----------
    id : int
        The primary key of the item.
    productid : int
        The id of the item.
    customerid : int
        The id of the customer who wrote it.
    rating : float
        The rating of the item.
    comment : str, optional
        The rating's description.
    moderation_status : str
        The number of items available in stock.
    """
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)
    moderation_status = Column(String, default="Pending")
