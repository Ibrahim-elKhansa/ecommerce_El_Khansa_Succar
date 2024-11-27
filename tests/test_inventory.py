import pytest
from fastapi.testclient import TestClient
from app_sales import app

client = TestClient(app)

@pytest.fixture
def setup_inventory():
    """
    Fixture to initialize test data for inventory.
    Adds a test item to the database before running tests.
    """
    client.post("/api/inventory", json={
        "name": "Test Item",
        "category": "Test Category",
        "price": 25.0,
        "description": "A sample test item",
        "stock_count": 5
    })


def test_add_item():
    """
    Test for adding a new item to the inventory.
    """
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
    """
    Test for listing all items in the inventory.
    """
    response = client.get("/api/inventory")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) > 0
    assert items[0]["name"] == "Test Item"


def test_get_item_details(setup_inventory):
    """
    Test for retrieving details of a specific item.
    """
    response = client.get("/api/inventory/1")
    assert response.status_code == 200
    item = response.json()
    assert item["name"] == "Test Item"
    assert item["category"] == "Test Category"
    assert item["price"] == 25.0
    assert item["stock_count"] == 5


def test_update_item(setup_inventory):
    """
    Test for updating an item's details.
    """
    response = client.put("/api/inventory/1", json={
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
    """
    Test for deducting stock from an item.
    """
    response = client.post("/api/inventory/1/deduct")
    assert response.status_code == 200
    assert response.json()["message"] == "Item deducted successfully"

    # Verify the stock count has decreased
    item_response = client.get("/api/inventory/1")
    assert item_response.status_code == 200
    item = item_response.json()
    assert item["stock_count"] == 4


def test_deduct_item_out_of_stock(setup_inventory):
    """
    Test for deducting stock from an item that is out of stock.
    """
    # Deduct all stock
    for _ in range(5):
        client.post("/api/inventory/1/deduct")

    # Attempt to deduct from out-of-stock item
    response = client.post("/api/inventory/1/deduct")
    assert response.status_code == 400
    assert response.json()["detail"] == "No stock available to deduct"
