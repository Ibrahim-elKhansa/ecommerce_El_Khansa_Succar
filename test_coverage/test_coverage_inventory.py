import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi.testclient import TestClient
from app_inventory.app_inventory import app

client = TestClient(app)

"""
Inventory Routes Test Module
============================

This module contains unit tests for the `inventory_routes` module of the FastAPI application.
It tests the API endpoints for inventory management, including creating, retrieving, updating,
deducting, and deleting inventory items.

Features
--------

- **Unit Tests**:
  - Test creating an inventory item.
  - Test retrieving all inventory items.
  - Test retrieving a specific inventory item by its ID.
  - Test updating an inventory item's details.
  - Test deducting stock from an inventory item.
  - Test deleting all inventory items.

Dependencies
------------

- **FastAPI TestClient**:
  Used to simulate API requests and responses.

Functions
---------

- `test_create_item()`:
    Tests the creation of a new inventory item via the `/api/items` endpoint.

- `test_get_all_items()`:
    Tests retrieving all inventory items using the `/api/items` endpoint.

- `test_get_item()`:
    Tests retrieving a specific inventory item by ID using the `/api/items/{item_id}` endpoint.

- `test_update_item()`:
    Tests updating an inventory item's details via the `/api/items/{item_id}` endpoint.

- `test_deduct_item()`:
    Tests deducting stock from an inventory item using the `/api/items/{item_id}/deduct` endpoint.

- `test_delete_all_items()`:
    Tests deleting all inventory items from the system using the `/api/items` endpoint.

"""


def test_create_item():
    """
    Test creating an inventory item.
    """
    data = {
        "name": "Sample Item",
        "category": "Sample Category",
        "price": 10.0,
        "description": "Sample Description",
        "stock_count": 5
    }
    response = client.post("/api/items", json=data)
    assert response.status_code == 200
    assert response.json()["item"]["name"] == "Sample Item"


def test_get_all_items():
    """
    Test retrieving all inventory items.
    """
    response = client.get("/api/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_item():
    """
    Test retrieving a specific inventory item by ID.
    """
    # First, create an item
    data = {
        "name": "Get Item Test",
        "category": "Test Category",
        "price": 20.0,
        "description": "Get Item Description",
        "stock_count": 3
    }
    create_response = client.post("/api/items", json=data)
    assert create_response.status_code == 200
    item_id = create_response.json()["item"]["id"]

    # Now, retrieve the item
    response = client.get(f"/api/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["id"] == item_id


def test_update_item():
    """
    Test updating an inventory item.
    """
    # First, create an item
    data = {
        "name": "Update Item Test",
        "category": "Update Category",
        "price": 30.0,
        "description": "Update Item Description",
        "stock_count": 7
    }
    create_response = client.post("/api/items", json=data)
    assert create_response.status_code == 200
    item_id = create_response.json()["item"]["id"]

    # Now, update the item
    updates = {"name": "Updated Item", "price": 35.0}
    update_response = client.put(f"/api/items/{item_id}", json=updates)
    assert update_response.status_code == 200
    assert update_response.json()["item"]["name"] == "Updated Item"


def test_deduct_item():
    """
    Test deducting stock from an inventory item.
    """
    # First, create an item
    data = {
        "name": "Deduct Item Test",
        "category": "Deduct Category",
        "price": 40.0,
        "description": "Deduct Item Description",
        "stock_count": 2
    }
    create_response = client.post("/api/items", json=data)
    assert create_response.status_code == 200
    item_id = create_response.json()["item"]["id"]

    # Deduct stock
    deduct_response = client.post(f"/api/items/{item_id}/deduct")
    assert deduct_response.status_code == 200
    assert deduct_response.json()["item"]["stock_count"] == 1


def test_delete_all_items():
    """
    Test deleting all inventory items.
    """
    # First, create a few items
    for i in range(3):
        data = {
            "name": f"Item {i}",
            "category": f"Category {i}",
            "price": 10.0 + i,
            "description": f"Description {i}",
            "stock_count": i + 1
        }
        client.post("/api/items", json=data)

    # Delete all items
    response = client.delete("/api/items")
    assert response.status_code == 200
    assert response.json()["message"] == "All items deleted successfully"

    # Verify all items are deleted
    response = client.get("/api/items")
    assert response.status_code == 200
    assert len(response.json()) == 0
