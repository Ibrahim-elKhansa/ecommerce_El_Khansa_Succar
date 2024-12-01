import sys
import os
from unittest.mock import patch
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_customer.app_customer import app

"""
Customer Routes Test Module
===========================

This module contains unit tests for the `customer_routes` module of the FastAPI application.
It uses the `unittest.mock` library to mock authentication dependencies and the `TestClient` 
from FastAPI to simulate API requests and responses.

Features
--------

- **Unit Tests**:
  - Test creating a customer.
  - Test retrieving a customer by username.
  - Test retrieving all customers.
  - Test updating a customer's details.
  - Test charging a customer's wallet.
  - Test deducting from a customer's wallet.
  - Test deleting a customer.

- **Mock Authentication**:
  - Authentication dependencies are mocked using the `unittest.mock.patch` decorator 
    to simulate authenticated users for testing purposes.

Dependencies
------------

- **FastAPI TestClient**:
  Used to send requests to the API endpoints.

- **Mocking**:
  The `get_current_user` dependency is mocked to bypass actual authentication.

Classes and Methods
-------------------

This module includes the following test functions:

- `test_create_customer(mock_auth)`:
  Tests the creation of a customer.
  
- `test_get_customer_by_username(mock_auth)`:
  Tests retrieving a customer by username.
  
- `test_get_all_customers(mock_auth)`:
  Tests retrieving all customers.

- `test_update_customer(mock_auth)`:
  Tests updating a customer's details.
  
- `test_charge_wallet(mock_auth)`:
  Tests charging a customer's wallet.

- `test_deduct_wallet(mock_auth)`:
  Tests deducting from a customer's wallet.
  
- `test_delete_customer(mock_auth)`:
  Tests deleting a customer and ensures the customer is no longer retrievable.

"""


client = TestClient(app)

@patch("routes.customer_routes.get_current_user", return_value={"id": 1, "username": "mock_user"})
def test_create_customer(mock_auth):
    """
    Test creating a customer.
    """
    data = {
        "full_name": "John Doe",
        "username": "johndoe",
        "password": "securepassword",
        "age": 30,
        "address": "123 Main St",
        "gender": "Male",
        "marital_status": "Single",
        "wallet_balance": 100.0
    }
    response = client.post("/api/customers", json=data)
    assert response.status_code == 200
    assert response.json()["customer"]["username"] == "johndoe"

@patch("routes.customer_routes.get_current_user", return_value={"id": 1, "username": "mock_user"})
def test_get_customer_by_username(mock_auth):
    """
    Test retrieving a customer by username.
    """
    response = client.get("/api/customers/johndoe")
    assert response.status_code == 200
    assert response.json()["username"] == "johndoe"

@patch("routes.customer_routes.get_current_user", return_value={"id": 1, "username": "mock_user"})
def test_get_all_customers(mock_auth):
    """
    Test retrieving all customers.
    """
    response = client.get("/api/customers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@patch("routes.customer_routes.get_current_user", return_value={"id": 1, "username": "mock_user"})
def test_update_customer(mock_auth):
    """
    Test updating a customer.
    """
    updates = {"address": "456 Elm St", "wallet_balance": 150.0}
    response = client.put("/api/customers/johndoe", json=updates)
    assert response.status_code == 200
    assert response.json()["customer"]["address"] == "456 Elm St"

@patch("routes.customer_routes.get_current_user", return_value={"id": 1, "username": "mock_user"})
def test_charge_wallet(mock_auth):
    """
    Test charging a customer's wallet.
    """
    response = client.post("/api/customers/johndoe/charge", json={"amount": 50.0})
    assert response.status_code == 200
    assert response.json()["customer"]["wallet_balance"] == 200.0

@patch("routes.customer_routes.get_current_user", return_value={"id": 1, "username": "mock_user"})
def test_deduct_wallet(mock_auth):
    """
    Test deducting from a customer's wallet.
    """
    response = client.post("/api/customers/johndoe/deduct", json={"amount": 50.0})
    assert response.status_code == 200
    assert response.json()["customer"]["wallet_balance"] == 150.0

@patch("routes.customer_routes.get_current_user", return_value={"id": 1, "username": "mock_user"})
def test_delete_customer(mock_auth):
    """
    Test deleting a customer.
    """
    response = client.delete("/api/customers/johndoe")
    assert response.status_code == 200
    assert response.json()["message"] == "Customer deleted successfully"

    # Verify the customer is deleted
    response = client.get("/api/customers/johndoe")
    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"
