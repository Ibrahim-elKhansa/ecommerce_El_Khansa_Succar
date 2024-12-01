from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Customer(Base):
    """
    SQLAlchemy model representing a customer in the application.

    Attributes
    ----------
    id : int
        The primary key of the customer.
    full_name : str
        The full name of the customer.
    username : str
        A unique username for the customer.
    password : str
        The password for the customer (stored as plain text; not recommended for production).
    age : int
        The age of the customer.
    address : str
        The address of the customer.
    gender : str
        The gender of the customer.
    marital_status : str
        The marital status of the customer (e.g., Single, Married).
    wallet_balance : float
        The current balance of the customer's wallet. Defaults to 0.0.
    is_admin : bool
        Indicates whether the customer has admin privileges. Defaults to False.
    """
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    address = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    marital_status = Column(String, nullable=False)
    wallet_balance = Column(Float, default=0.0)
    is_admin = Column(Boolean, default=False)