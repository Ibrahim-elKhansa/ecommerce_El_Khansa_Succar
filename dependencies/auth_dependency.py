from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime
from decouple import config
from models.customer import Customer
from database import get_db

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = "HS256"
ADMIN_TOKEN = config("ADMIN_TOKEN")

security = HTTPBearer()


def decode_jwt(token: str) -> dict:
    """
    Decodes the JWT token and returns the payload if valid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("exp") and datetime.utcnow().timestamp() > payload["exp"]:
            raise JWTError("Token has expired")
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> dict:
    """
    Verifies the token and returns the user information from the payload.
    """
    token = credentials.credentials

    # If the token matches the static admin token, authorize directly as admin
    if token == ADMIN_TOKEN:
        return {"sub": "admin", "role": "admin"}

    # Otherwise, proceed with normal JWT validation
    try:
        payload = decode_jwt(token)
        if not payload or "sub" not in payload:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return payload
    except JWTError as e:
        if token == ADMIN_TOKEN:  # Re-check in case the exception occurs
            return {"sub": "admin", "role": "admin"}
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")


def require_admin(
    current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Ensure the current user is an admin by querying the database or checking the static token.
    """
    # If the static admin token is used, it is already validated
    if current_user.get("role") == "admin":
        return current_user

    # For regular tokens, validate admin status from the database
    user = db.query(Customer).filter(Customer.username == current_user["sub"]).first()
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user
