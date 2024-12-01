from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.auth_service import AuthService
from database import get_db
from schemas.customer_schema import CustomerCreate, CustomerResponse
from pydantic import BaseModel

router = APIRouter()
auth_service = AuthService()

class LoginRequest(BaseModel):
    """
    Represents the data required for a login request.

    Attributes:
        username (str): The username of the customer.
        password (str): The password of the customer.
    """
    username: str
    password: str

@router.post("/register", response_model=CustomerResponse)
def register(customer_data: CustomerCreate, db: Session = Depends(get_db)):
    """
    Registers a new customer.

    Args:
        customer_data (CustomerCreate): The data required to create a customer.
        db (Session): The database session dependency.

    Returns:
        CustomerResponse: The newly created customer data.

    Raises:
        HTTPException: If customer creation fails.
    """
    try:
        new_customer = auth_service.register(db, customer_data.dict())
        return new_customer
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(request: LoginRequest):
    """
    Authenticates a customer and provides an access token.

    Args:
        request (LoginRequest): The login request containing username and password.

    Returns:
        dict: The access token if authentication is successful.

    Raises:
        HTTPException: If login fails.
    """
    return auth_service.login(username=request.username, password=request.password)
