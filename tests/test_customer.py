import pytest
from fastapi.testclient import TestClient
from app_customer import app

client = TestClient(app)

def test_register_customer():
    response = client.post("/customers", json={
        "full_name": "John Doe",
        "username": "johndoe",
        "password": "securepassword",
        "age": 30,
        "address": "123 Main St",
        "gender": "Male",
        "marital_status": "Single"
    })
    assert response.status_code == 200
    
    assert response.json()["username"] == "johndoe"

def test_get_customer():
    response = client.get("/customers/johndoe")
    assert response.status_code == 200
    assert response.json()["username"] == "johndoe"

def test_charge_customer():
    response = client.post("/customers/johndoe/charge", json={"amount": 100.0})
    assert response.status_code == 200
    assert response.json()["wallet_balance"] == 100.0

def test_deduct_customer():
    response = client.post("/customers/johndoe/deduct", json={"amount": 50.0})
    assert response.status_code == 200
    assert response.json()["wallet_balance"] == 50.0
