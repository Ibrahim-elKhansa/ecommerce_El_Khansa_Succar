from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String)
    stock_count = Column(Integer, nullable=False)

    sales = relationship("Sale", back_populates="item")

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    wallet_balance = Column(Float, default=0.0)

    sales = relationship("Sale", back_populates="customer")

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    amount = Column(Float, nullable=False)

    customer = relationship("Customer", back_populates="sales")
    item = relationship("Item", back_populates="sales")
