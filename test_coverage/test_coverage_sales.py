import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi.testclient import TestClient
from app_sales.app_sales import app

client = TestClient(app)

"""
Sales Routes Test Module
========================

This module contains unit tests for the `sales_routes` module of the FastAPI application.
It verifies the functionality of the sales management endpoints, including creating, retrieving,
updating, and deleting sales.

Features
--------

- **Unit Tests**:
  - Test creating a new sale.
  - Test retrieving sales by customer ID.
  - Test retrieving sales by item ID.
  - Test updating an existing sale.
  - Test deleting a sale.

Dependencies
------------

- **FastAPI TestClient**:
  Used to simulate API requests and responses.

- **Routes**:
  - The `sales_routes` module handles all sales-related operations.

Functions
---------

- `test_create_sale()`:
    Tests creating a new sale using the `/api/sales` endpoint.

- `test_get_sales_by_customer()`:
    Tests retrieving sales associated with a customer via the `/api/sales/customer/{customer_id}` endpoint.

- `test_get_sales_by_item()`:
    Tests retrieving sales associated with an item via the `/api/sales/item/{item_id}` endpoint.

- `test_update_sale()`:
    Tests updating an existing sale record using the `/api/sales/{sale_id}` endpoint.

- `test_delete_sale()`:
    Tests deleting a sale record via the `/api/sales/{sale_id}` endpoint.

"""


def test_create_sale():
    """
    Test creating a sale.
    """
    data = {"customer_id": 1, "item_id": 1, "amount": 100.0}
    response = client.post("/api/sales", json=data)
    assert response.status_code == 200
    assert response.json()["sale"]["customer_id"] == 1
    assert response.json()["sale"]["item_id"] == 1
    assert response.json()["sale"]["amount"] == 100.0

def test_get_sales_by_customer():
    """
    Test retrieving sales by customer ID.
    """
    response = client.get("/api/sales/customer/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_sales_by_item():
    """
    Test retrieving sales by item ID.
    """
    response = client.get("/api/sales/item/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_sale():
    """
    Test updating a sale.
    """
    updates = {"amount": 200.0}
    response = client.put("/api/sales/1", json=updates)
    assert response.status_code == 200
    assert response.json()["sale"]["amount"] == 200.0

def test_delete_sale():
    """
    Test deleting a sale.
    """
    response = client.delete("/api/sales/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Sale deleted successfully"
