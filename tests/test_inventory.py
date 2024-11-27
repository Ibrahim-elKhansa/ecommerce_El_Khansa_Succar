import pytest
from fastapi.testclient import TestClient
from app_inventory import app

client = TestClient(app)

def test_add_item():
    response = client.post("/api/inventory", json={
        "name": "Laptop",
        "category": "Electronics",
        "price": 999.99,
        "description": "A high-performance laptop",
        "stock_count": 10
    })
    assert response.status_code == 200
    assert response.json()["item"]["name"] == "Laptop"

def test_get_all_items():
    response = client.get("/api/inventory")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_item_details():
    response = client.get("/api/inventory/1")  # Assuming item ID = 1 exists
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"

def test_update_item():
    response = client.put("/api/inventory/1", json={
        "stock_count": 20,
        "price": 899.99
    })
    assert response.status_code == 200
    assert response.json()["item"]["stock_count"] == 20

def test_deduct_item():
    response = client.post("/api/inventory/1/deduct")
    assert response.status_code == 200
    response = client.get("/api/inventory/1")
    assert response.json()["stock_count"] == 19
