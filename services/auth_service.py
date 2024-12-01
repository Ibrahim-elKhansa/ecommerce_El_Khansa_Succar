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
    username: str

class AuthService:
    def __init__(self):
        self.db = SessionLocal()

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token payload")
            return TokenData(username=username)
        except JWTError:
            raise HTTPException(status_code=401, detail="Could not validate token")

    def register(self, db: Session, customer_data: dict):
        existing_customer = db.query(Customer).filter(Customer.username == customer_data['username']).first()
        if existing_customer:
            raise HTTPException(status_code=400, detail="Username already exists")

        new_customer = Customer(**customer_data)
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        return new_customer

    def login(self, username: str, password: str):
        user = self.db.query(Customer).filter(Customer.username == username).first()
        if not user or user.password != password:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        access_token = self.create_access_token(data={"sub": username})
        return {"access_token": access_token, "token_type": "bearer"}
