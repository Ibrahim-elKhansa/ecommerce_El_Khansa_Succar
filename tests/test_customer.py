import sys
import os
import pytest
from line_profiler import LineProfiler
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app_customer import app
from services.customer_service import (
    create_customer,
    charge_wallet,
    deduct_wallet,
    delete_customer,
)

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_customer():
    client.post("/api/customers", json={
        "full_name": "John Doe",
        "username": "johndoe",
        "password": "securepassword",
        "age": 30,
        "address": "123 Main St",
        "gender": "Male",
        "marital_status": "Single"
    })
    yield

def test_register_customer(setup_customer):
    response = client.get("/api/customers/johndoe")
    assert response.status_code == 200
    assert response.json()["username"] == "johndoe"

def test_charge_customer(setup_customer):
    # Add line profiling
    lp = LineProfiler()
    lp.add_function(charge_wallet.__wrapped__)  # Use the wrapped function

    @lp
    def execute():
        response = client.post("/api/customers/johndoe/charge", json={"amount": 100.0})
        assert response.status_code == 200
        assert response.json()["wallet_balance"] == 100.0

    execute()
    lp.print_stats()

def test_deduct_customer(setup_customer):
    # Add line profiling
    lp = LineProfiler()
    lp.add_function(deduct_wallet.__wrapped__)  # Use the wrapped function

    @lp
    def execute():
        response = client.post("/api/customers/johndoe/deduct", json={"amount": 50.0})
        assert response.status_code == 200
        assert response.json()["wallet_balance"] == 50.0

    execute()
    lp.print_stats()

def test_delete_customer(setup_customer):
    # Add line profiling
    lp = LineProfiler()
    lp.add_function(delete_customer.__wrapped__)  # Use the wrapped function

    @lp
    def execute():
        # Delete the user
        response = client.delete("/api/customers/johndoe")
        assert response.status_code == 200
        assert response.json()["message"] == "Customer deleted successfully"

        # Verify the user is deleted
        response = client.get("/api/customers/johndoe")
        assert response.status_code == 404
        assert response.json()["detail"] == "Customer not found"

    execute()
    lp.print_stats()
