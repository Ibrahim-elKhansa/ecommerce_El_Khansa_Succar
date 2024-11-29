import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi.testclient import TestClient
from app_sales import app
from line_profiler import LineProfiler

client = TestClient(app)

def test_create_sale():
    lp = LineProfiler()
    lp.add_function(client.post)
    
    @lp
    def execute():
        data = {"customer_id": 1, "item_id": 1, "amount": 100.0}
        response = client.post("api/sales", json=data)
        assert response.status_code == 200
        assert response.json()["sale"]["customer_id"] == 1
        assert response.json()["sale"]["item_id"] == 1
        assert response.json()["sale"]["amount"] == 100.0
    
    execute()
    lp.print_stats()

def test_get_sales_by_customer():
    lp = LineProfiler()
    lp.add_function(client.get)

    @lp
    def execute():
        response = client.get("api/sales/customer/1")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    execute()
    lp.print_stats()

def test_get_sales_by_item():
    lp = LineProfiler()
    lp.add_function(client.get)

    @lp
    def execute():
        response = client.get("api/sales/item/1")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    execute()
    lp.print_stats()

def test_update_sale():
    lp = LineProfiler()
    lp.add_function(client.put)

    @lp
    def execute():
        updates = {"amount": 200.0}
        response = client.put("api/sales/1", json=updates)
        assert response.status_code == 200
        assert response.json()["sale"]["amount"] == 200.0

    execute()
    lp.print_stats()

def test_delete_sale():
    lp = LineProfiler()
    lp.add_function(client.delete)

    @lp
    def execute():
        response = client.delete("api/sales/1")
        assert response.status_code == 200
        assert response.json()["message"] == "Sale deleted successfully"

    execute()
    lp.print_stats()
