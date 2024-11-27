from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False)
    customer_id = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    comment = Column(String, nullable=True)
    moderated = Column(String, default="Pending")
