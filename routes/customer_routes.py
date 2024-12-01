import os
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.customer_service import CustomerService
from dependencies.auth_dependency import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

os.makedirs("logs", exist_ok=True)  # Ensure logs directory exists
logging.basicConfig(
    filename="logs/log_customer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

limiter = Limiter(key_func=get_remote_address)  # Throttling mechanism
router = APIRouter()
customer_service = CustomerService() 

@router.post("/customers", dependencies=[Depends(get_current_user)])
def create_customer_route(customer_data: dict, db: Session = Depends(get_db)):
    """
    Create a new customer.

    Args:
        customer_data (dict): The data required to create a customer.
        db (Session): The database session dependency.

    Returns:
        dict: A message and the created customer data.

    Raises:
        HTTPException: If the customer creation fails.
    """
    logging.info(f"POST /customers - Data: {customer_data}")
    try:
        new_customer = customer_service.create_customer(db, customer_data)
        logging.info(f"Customer created: {new_customer}")
        return {"message": "Customer created successfully", "customer": new_customer}
    except ValueError as e:
        logging.error(f"Error creating customer: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/customers/{username}", dependencies=[Depends(get_current_user)])
def get_customer_by_username(username: str, db: Session = Depends(get_db)):
    """
    Retrieve a customer by username.

    Args:
        username (str): The username of the customer to retrieve.
        db (Session): The database session dependency.

    Returns:
        dict: The retrieved customer data.

    Raises:
        HTTPException: If the customer is not found.
    """
    username = username.strip()
    logging.info(f"GET /customers/{username}")
    customer = customer_service.get_customer_by_username(db, username)
    if not customer:
        logging.warning(f"Customer not found: {username}")
        raise HTTPException(status_code=404, detail="Customer not found")
    logging.info(f"Customer retrieved: {customer}")
    return customer

@router.get("/customers", dependencies=[Depends(get_current_user)])
def get_all_customers_route(db: Session = Depends(get_db)):
    """
    Retrieve all customers.

    Args:
        db (Session): The database session dependency.

    Returns:
        list: A list of all customers.
    """
    logging.info("GET /customers")
    customers = customer_service.get_all_customers(db)
    logging.info(f"All customers retrieved: {len(customers)} customers")
    return customers

@router.put("/customers/{username}", dependencies=[Depends(get_current_user)])
def update_customer_route(username: str, updates: dict, db: Session = Depends(get_db)):
    """
    Update a customer's information.

    Args:
        username (str): The username of the customer to update.
        updates (dict): The updates to apply to the customer.
        db (Session): The database session dependency.

    Returns:
        dict: A message and the updated customer data.

    Raises:
        HTTPException: If the update fails.
    """
    username = username.strip()
    logging.info(f"PUT /customers/{username} - Updates: {updates}")
    try:
        updated_customer = customer_service.update_customer(db, username, updates)
        logging.info(f"Customer updated: {updated_customer}")
        return {"message": "Customer updated successfully", "customer": updated_customer}
    except ValueError as e:
        logging.error(f"Error updating customer {username}: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/customers/{username}", dependencies=[Depends(get_current_user)])
def delete_customer_route(username: str, db: Session = Depends(get_db)):
    """
    Delete a customer by username.

    Args:
        username (str): The username of the customer to delete.
        db (Session): The database session dependency.

    Returns:
        dict: A message confirming deletion.

    Raises:
        HTTPException: If the deletion fails.
    """
    username = username.strip()
    logging.info(f"DELETE /customers/{username}")
    try:
        customer_service.delete_customer(db, username)
        logging.info(f"Customer deleted: {username}")
        return {"message": "Customer deleted successfully"}
    except ValueError as e:
        logging.error(f"Error deleting customer {username}: {e}")
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/customers/{username}/charge", dependencies=[Depends(get_current_user)])
def charge_wallet_route(username: str, data: dict, db: Session = Depends(get_db)):
    """
    Charge a customer's wallet.

    Args:
        username (str): The username of the customer to charge.
        data (dict): Contains the 'amount' to charge.
        db (Session): The database session dependency.

    Returns:
        dict: A message and the updated customer data.

    Raises:
        HTTPException: If the 'amount' key is missing or the charge fails.
    """
    print([username])
    try:
        amount = data["amount"]
        charged_customer = customer_service.charge_wallet(db, username, amount)
        logging.info(f"Wallet charged for {username}: {charged_customer}")
        return {"message": "Wallet charged successfully", "customer": charged_customer}
    except KeyError as e:
        logging.error(f"KeyError: {e}")
        raise HTTPException(status_code=422, detail=f"Missing 'amount' in request data: {e}")
    except ValueError as e:
        logging.error(f"Error charging wallet for {username}: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/customers/{username}/deduct", dependencies=[Depends(get_current_user)])
def deduct_wallet_route(username: str, data: dict, db: Session = Depends(get_db)):
    """
    Deduct an amount from a customer's wallet.

    Args:
        username (str): The username of the customer.
        data (dict): Contains the 'amount' to deduct.
        db (Session): The database session dependency.

    Returns:
        dict: A message and the updated customer data.

    Raises:
        HTTPException: If the deduction fails.
    """
    amount = data["amount"]
    logging.info(f"POST /customers/{username}/deduct - Amount: {amount}")
    try:
        deducted_customer = customer_service.deduct_wallet(db, username, amount)
        logging.info(f"Wallet deducted for customer {username}: {deducted_customer}")
        return {"message": "Wallet deducted successfully", "customer": deducted_customer}
    except ValueError as e:
        logging.error(f"Error deducting wallet for {username}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
