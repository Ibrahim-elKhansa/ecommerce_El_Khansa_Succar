from sqlalchemy import Column, Integer, Float
from database import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, nullable=False)
    item_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
