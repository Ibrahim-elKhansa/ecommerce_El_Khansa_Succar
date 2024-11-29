import pytest
import sys, os
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app_inventory import app

client = TestClient(app)

@pytest.fixture
def setup_inventory():
    """
    Fixture to initialize test data for inventory.
    Cleans up and adds a test item to the database before running tests.
    """
    client.delete("/api/inventory/all")
    response = client.post("/api/inventory", json={
        "name": "Test Item",
        "category": "Test Category",
        "price": 25.0,
        "description": "A sample test item",
        "stock_count": 5
    })
    return response.json()["item"]["id"]

def test_add_item():
    client.delete("/api/inventory/all")
    response = client.post("/api/inventory", json={
        "name": "New Item",
        "category": "Electronics",
        "price": 100.0,
        "description": "A new item for testing",
        "stock_count": 10
    })
    assert response.status_code == 200
    item = response.json()
    assert item["message"] == "Item added successfully"
    assert item["item"]["name"] == "New Item"

def test_list_items(setup_inventory):
    item_id = setup_inventory
    response = client.get("/api/inventory")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) > 0
    assert items[0]["name"] == "Test Item"

def test_get_item_details(setup_inventory):
    item_id = setup_inventory
    response = client.get(f"/api/inventory/{item_id}")
    assert response.status_code == 200
    item = response.json()
    assert item["name"] == "Test Item"
    assert item["category"] == "Test Category"
    assert item["price"] == 25.0
    assert item["stock_count"] == 5

def test_update_item(setup_inventory):
    item_id = setup_inventory
    response = client.put(f"/api/inventory/{item_id}", json={
        "name": "Updated Item",
        "category": "Updated Category",
        "price": 50.0,
        "description": "Updated description",
        "stock_count": 10
    })
    assert response.status_code == 200
    updated_item = response.json()["item"]
    assert updated_item["name"] == "Updated Item"
    assert updated_item["price"] == 50.0
    assert updated_item["stock_count"] == 10

def test_deduct_item(setup_inventory):
    item_id = setup_inventory
    response = client.post(f"/api/inventory/{item_id}/deduct")
    assert response.status_code == 200
    assert response.json()["message"] == "Item deducted successfully"
    item_response = client.get(f"/api/inventory/{item_id}")
    assert item_response.status_code == 200
    item = item_response.json()
    assert item["stock_count"] == 4

def test_deduct_item_out_of_stock(setup_inventory):
    item_id = setup_inventory
    for _ in range(5):
        client.post(f"/api/inventory/{item_id}/deduct")
    response = client.post(f"/api/inventory/{item_id}/deduct")
    assert response.status_code == 400
    assert response.json()["detail"] == "No stock available to deduct"
