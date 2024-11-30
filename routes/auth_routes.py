from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.auth_service import AuthService
from database import get_db
from schemas.customer_schema import CustomerCreate, CustomerResponse
from pydantic import BaseModel

router = APIRouter()
auth_service = AuthService()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/register", response_model=CustomerResponse)
def register(customer_data: CustomerCreate, db: Session = Depends(get_db)):
    try:
        new_customer = auth_service.register(db, customer_data.dict())
        return new_customer
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(request: LoginRequest):
    return auth_service.login(username=request.username, password=request.password)
