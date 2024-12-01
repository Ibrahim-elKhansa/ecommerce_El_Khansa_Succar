import sys
import os
from unittest.mock import patch
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_customer.app_customer import app

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
