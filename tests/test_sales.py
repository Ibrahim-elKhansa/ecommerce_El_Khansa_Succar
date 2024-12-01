import sys
import os
from decouple import config
from fastapi.testclient import TestClient
from line_profiler import LineProfiler

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app_sales import app

client = TestClient(app)

# Load the admin token from .env
ADMIN_TOKEN = config("ADMIN_TOKEN")

# Add the Authorization header for all requests
HEADERS = {"Authorization": f"Bearer {ADMIN_TOKEN}"}

def test_create_sale():
    """
    Test creating a sale.

    - Profiles the `client.post` method to evaluate performance.
    - Sends a POST request to create a new sale.
    - Verifies that the sale is successfully created with the correct details.
    """
    lp = LineProfiler()
    lp.add_function(client.post)
    
    @lp
    def execute():
        data = {"customer_id": 1, "item_id": 1, "amount": 100.0}
        response = client.post("api/sales", json=data, headers=HEADERS)
        assert response.status_code == 200
        assert response.json()["sale"]["customer_id"] == 1
        assert response.json()["sale"]["item_id"] == 1
        assert response.json()["sale"]["amount"] == 100.0
    
    execute()
    lp.print_stats()

def test_get_sales_by_customer():
    """
    Test retrieving sales for a specific customer.

    - Profiles the `client.get` method to evaluate performance.
    - Sends a GET request to fetch sales by customer ID.
    - Verifies that the response contains a list of sales.
    """
    lp = LineProfiler()
    lp.add_function(client.get)

    @lp
    def execute():
        response = client.get("api/sales/customer/1", headers=HEADERS)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    execute()
    lp.print_stats()

def test_get_sales_by_item():
    """
    Test retrieving sales for a specific item.

    - Profiles the `client.get` method to evaluate performance.
    - Sends a GET request to fetch sales by item ID.
    - Verifies that the response contains a list of sales.
    """
    lp = LineProfiler()
    lp.add_function(client.get)

    @lp
    def execute():
        response = client.get("api/sales/item/1", headers=HEADERS)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    execute()
    lp.print_stats()

def test_update_sale():
    """
    Test updating an existing sale.

    - Profiles the `client.put` method to evaluate performance.
    - Sends a PUT request to update the amount of a sale.
    - Verifies that the sale details are updated correctly.
    """
    lp = LineProfiler()
    lp.add_function(client.put)

    @lp
    def execute():
        updates = {"amount": 200.0}
        response = client.put("api/sales/1", json=updates, headers=HEADERS)
        assert response.status_code == 200
        assert response.json()["sale"]["amount"] == 200.0

    execute()
    lp.print_stats()

def test_delete_sale():
    """
    Test deleting a sale.

    - Profiles the `client.delete` method to evaluate performance.
    - Sends a DELETE request to remove a specific sale.
    - Verifies that the sale is deleted successfully with the appropriate message.
    """
    lp = LineProfiler()
    lp.add_function(client.delete)

    @lp
    def execute():
        response = client.delete("api/sales/1", headers=HEADERS)
        assert response.status_code == 200
        assert response.json()["message"] == "Sale deleted successfully"

    execute()
    lp.print_stats()
