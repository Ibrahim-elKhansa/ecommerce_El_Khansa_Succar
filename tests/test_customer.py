import sys
import os
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app_customer import app

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_customer():
    client.post("/api/customers", json={
        "full_name": "John Doe",
        "username": "johndoe",
        "password": "securepassword",
        "age": 30,
        "address": "123 Main St",
        "gender": "Male",
        "marital_status": "Single"
    })
    yield

def test_register_customer(setup_customer):
    response = client.get("/api/customers/johndoe")
    assert response.status_code == 200
    assert response.json()["username"] == "johndoe"

def test_charge_customer(setup_customer):
    response = client.post("/api/customers/johndoe/charge", json={"amount": 100.0})
    assert response.status_code == 200
    assert response.json()["wallet_balance"] == 100.0

def test_deduct_customer(setup_customer):
    response = client.post("/api/customers/johndoe/deduct", json={"amount": 50.0})
    assert response.status_code == 200
    assert response.json()["wallet_balance"] == 50.0

def test_delete_customer(setup_customer):
    # Delete the user
    response = client.delete("/api/customers/johndoe")
    assert response.status_code == 200
    assert response.json()["message"] == "Customer deleted successfully"

    # Verify the user is deleted
    response = client.get("/api/customers/johndoe")
    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"
