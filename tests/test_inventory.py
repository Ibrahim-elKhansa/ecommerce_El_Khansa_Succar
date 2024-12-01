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
    """
    Test adding a new item to the inventory.

    - Verifies that the item is created successfully.
    - Checks that the item data matches the expected values.
    """
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
    """
    Test listing all items in the inventory.

    - Adds a sample item to the inventory.
    - Verifies that the item appears in the list of all items.
    """
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
    """
    Test retrieving details of a specific item.

    - Adds a sample item to the inventory.
    - Verifies that the details of the item match the expected values.
    """
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
    """
    Test updating an existing item's details.

    - Adds a sample item to the inventory.
    - Updates the item's details and verifies the changes.
    """
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
    """
    Test deducting stock from an item.

    - Adds a sample item to the inventory.
    - Deducts stock and verifies the response.
    """
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
    """
    Test deducting stock from an item when stock is unavailable.

    - Adds a sample item to the inventory with limited stock.
    - Attempts to deduct stock beyond the available quantity.
    - Verifies that the appropriate error message is returned.
    """
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
