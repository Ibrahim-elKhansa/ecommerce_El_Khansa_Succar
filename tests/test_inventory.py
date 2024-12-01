import pytest
import sys, os
from fastapi.testclient import TestClient
from decouple import config

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app_inventory import app

client = TestClient(app)

# Load the admin token from .env
ADMIN_TOKEN = config("ADMIN_TOKEN")

# Add the Authorization header for all requests
HEADERS = {"Authorization": f"Bearer {ADMIN_TOKEN}"}

@pytest.fixture(autouse=True)
def cleanup_inventory():
    """
    Automatically clean up inventory before each test.
    """
    client.delete("/api/items", headers=HEADERS)

def test_add_item():
    response = client.post(
        "/api/items",
        json={
            "name": "New Item",
            "category": "Electronics",
            "price": 100.0,
            "description": "A new item for testing",
            "stock_count": 10,
        },
        headers=HEADERS,
    )
    assert response.status_code == 200
    item = response.json()["item"]
    assert item["name"] == "New Item"

def test_list_items():
    response = client.post(
        "/api/items",
        json={
            "name": "Test Item",
            "category": "Test Category",
            "price": 25.0,
            "description": "A sample test item",
            "stock_count": 5,
        },
        headers=HEADERS,
    )
    response = client.get("/api/items", headers=HEADERS)
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert any(item["name"] == "Test Item" for item in items)

def test_get_item_details():
    response = client.post(
        "/api/items",
        json={
            "name": "Test Item",
            "category": "Test Category",
            "price": 25.0,
            "description": "A sample test item",
            "stock_count": 5,
        },
        headers=HEADERS,
    )
    item_id = response.json()["item"]["id"]
    response = client.get(f"/api/items/{item_id}", headers=HEADERS)
    assert response.status_code == 200
    item = response.json()
    assert item["name"] == "Test Item"

def test_update_item():
    response = client.post(
        "/api/items",
        json={
            "name": "Test Item",
            "category": "Test Category",
            "price": 25.0,
            "description": "A sample test item",
            "stock_count": 5,
        },
        headers=HEADERS,
    )
    item_id = response.json()["item"]["id"]
    response = client.put(
        f"/api/items/{item_id}",
        json={
            "name": "Updated Item",
            "category": "Updated Category",
            "price": 50.0,
            "description": "Updated description",
            "stock_count": 10,
        },
        headers=HEADERS,
    )
    assert response.status_code == 200
    updated_item = response.json()["item"]
    assert updated_item["name"] == "Updated Item"

def test_deduct_item():
    response = client.post(
        "/api/items",
        json={
            "name": "Test Item",
            "category": "Test Category",
            "price": 25.0,
            "description": "A sample test item",
            "stock_count": 5,
        },
        headers=HEADERS,
    )
    item_id = response.json()["item"]["id"]
    response = client.post(f"/api/items/{item_id}/deduct", headers=HEADERS)
    assert response.status_code == 200

def test_deduct_item_out_of_stock():
    response = client.post(
        "/api/items",
        json={
            "name": "Test Item",
            "category": "Test Category",
            "price": 25.0,
            "description": "A sample test item",
            "stock_count": 5,
        },
        headers=HEADERS,
    )
    item_id = response.json()["item"]["id"]
    for _ in range(5):
        client.post(f"/api/items/{item_id}/deduct", headers=HEADERS)
    response = client.post(f"/api/items/{item_id}/deduct", headers=HEADERS)
    assert response.status_code == 400
    assert response.json()["detail"] == "No stock available to deduct"
