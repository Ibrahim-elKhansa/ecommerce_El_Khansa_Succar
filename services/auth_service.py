from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException
from pydantic import BaseModel
from models.customer import Customer
from database import SessionLocal
from sqlalchemy.orm import Session
from schemas.customer_schema import CustomerResponse
from decouple import config

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)

class TokenData(BaseModel):
    """
    Pydantic model for token data.

    Attributes:
        username (str): The username embedded in the token.
    """
    username: str

class AuthService:
    """
    Service class for authentication and user management.

    Methods:
        create_access_token(data: dict) -> str:
            Generates a JWT access token with an expiration time.
        
        verify_token(token: str):
            Verifies and decodes the provided JWT token.
        
        register(db: Session, customer_data: dict):
            Registers a new customer in the database.
        
        login(username: str, password: str):
            Authenticates a user and generates an access token.
    """
    def __init__(self):
        self.db = SessionLocal()

    def create_access_token(self, data: dict) -> str:
        """
        Generates a JWT access token with an expiration time.

        Args:
            data (dict): The data to encode in the token.

        Returns:
            str: The generated JWT access token.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def verify_token(self, token: str):
        """
        Verifies and decodes the provided JWT token.

        Args:
            token (str): The JWT token to verify.

        Returns:
            TokenData: The decoded token data.

        Raises:
            HTTPException: If the token is invalid or cannot be verified.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token payload")
            return TokenData(username=username)
        except JWTError:
            raise HTTPException(status_code=401, detail="Could not validate token")

    def register(self, db: Session, customer_data: dict):
        """
        Registers a new customer in the database.

        Args:
            db (Session): The database session.
            customer_data (dict): The customer data to register.

        Returns:
            Customer: The registered customer instance.

        Raises:
            HTTPException: If the username already exists.
        """
        existing_customer = db.query(Customer).filter(Customer.username == customer_data['username']).first()
        if existing_customer:
            raise HTTPException(status_code=400, detail="Username already exists")

        new_customer = Customer(**customer_data)
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        return new_customer

    def login(self, username: str, password: str):
        """
        Authenticates a user and generates an access token.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            dict: A dictionary containing the access token and token type.

        Raises:
            HTTPException: If the username or password is invalid.
        """
        user = self.db.query(Customer).filter(Customer.username == username).first()
        if not user or user.password != password:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        access_token = self.create_access_token(data={"sub": username})
        return {"access_token": access_token, "token_type": "bearer"}
