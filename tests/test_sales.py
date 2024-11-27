import pytest
import sys, os
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app_sales import app
client = TestClient(app)

@pytest.fixture
def setup_test_data():
    """
    Fixture to initialize test data for sales.
    Adds a test customer and item to the database before running tests.
    """
    client.post("/api/customers", json={
        "username": "testuser",
        "wallet_balance": 100.0
    })

    client.post("/api/inventory", json={
        "name": "Test Item",
        "category": "Test Category",
        "price": 50.0,
        "description": "A test item description",
        "stock_count": 10
    })


def test_display_goods(setup_test_data):
    """
    Test for displaying all goods.
    """
    response = client.get("/api/sales/goods")
    assert response.status_code == 200
    goods = response.json()
    assert isinstance(goods, list)
    assert len(goods) > 0
    assert goods[0]["name"] == "Test Item"
    assert goods[0]["price"] == 50.0


def test_get_good_details(setup_test_data):
    """
    Test for retrieving details of a specific good.
    """
    response = client.get("/api/sales/goods/1")
    assert response.status_code == 200
    item = response.json()
    assert item["name"] == "Test Item"
    assert item["category"] == "Test Category"
    assert item["price"] == 50.0
    assert item["stock_count"] == 10


def test_process_sale(setup_test_data):
    """
    Test for processing a sale.
    """
    response = client.post("/api/sales/testuser", json={"item_id": 1})
    assert response.status_code == 200
    sale = response.json()
    assert sale["customer_username"] == "testuser"
    assert sale["item_name"] == "Test Item"
    assert sale["amount"] == 50.0

    item_response = client.get("/api/sales/goods/1")
    assert item_response.status_code == 200
    item = item_response.json()
    assert item["stock_count"] == 9

    customer_response = client.get("/api/customers/testuser")
    assert customer_response.status_code == 200
    customer = customer_response.json()
    assert customer["wallet_balance"] == 50.0


def test_process_sale_insufficient_funds(setup_test_data):
    """
    Test for processing a sale with insufficient funds.
    """
    client.put("/api/customers/testuser", json={"wallet_balance": 10.0})

    response = client.post("/api/sales/testuser", json={"item_id": 1})
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient funds"


def test_process_sale_out_of_stock(setup_test_data):
    """
    Test for processing a sale when the item is out of stock.
    """
    for _ in range(10):
        client.post("/api/sales/testuser", json={"item_id": 1})

    response = client.post("/api/sales/testuser", json={"item_id": 1})
    assert response.status_code == 400
    assert response.json()["detail"] == "Item is out of stock"
