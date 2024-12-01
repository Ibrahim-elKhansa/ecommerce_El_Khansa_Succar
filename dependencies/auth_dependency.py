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
    Decodes a JWT token and validates its payload.

    Args:
        token (str): The JWT token to decode.

    Returns:
        dict: Decoded JWT payload.

    Raises:
        HTTPException: If the token is invalid or expired.
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
    Validates the authorization token and retrieves the current user.

    Args:
        credentials (HTTPAuthorizationCredentials): Bearer token credentials.

    Returns:
        dict: Payload containing user information.

    Raises:
        HTTPException: If the token is invalid or the payload is missing required data.
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
    Ensures the current user is an admin.

    Args:
        current_user (dict): The currently authenticated user data.
        db (Session): Database session for querying user details.

    Returns:
        dict: The current user information if they are an admin.

    Raises:
        HTTPException: If the user is not an admin or is unauthorized.
    """
    # If the static admin token is used, it is already validated
    if current_user.get("role") == "admin":
        return current_user

    # For regular tokens, validate admin status from the database
    user = db.query(Customer).filter(Customer.username == current_user["sub"]).first()
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user
