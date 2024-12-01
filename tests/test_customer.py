import pytest
import sys, os
from fastapi.testclient import TestClient
from decouple import config
from line_profiler import LineProfiler

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app_customer.app_customer import app
from services.customer_service import CustomerService

client = TestClient(app)

# Load the admin token from .env
ADMIN_TOKEN = config("ADMIN_TOKEN")

# Add the Authorization header for all requests
HEADERS = {"Authorization": f"Bearer {ADMIN_TOKEN}"}

@pytest.fixture(scope="module")
def setup_customer():
    """
    Fixture to initialize test data for customer.
    Cleans up and adds a test customer to the database before running tests.
    """
    client.delete("/api/customers/johndoe", headers=HEADERS)
    response = client.post(
        "/api/customers",
        json={
            "full_name": "John Doe",
            "username": "johndoe",
            "password": "securepassword",
            "age": 30,
            "address": "123 Main St",
            "gender": "Male",
            "marital_status": "Single",
        },
        headers=HEADERS,
    )
    assert response.status_code == 200
    yield

def test_register_customer(setup_customer):
    """
    Test retrieving a registered customer by username.
    
    - Verifies that the customer data matches the expected values.
    """
    response = client.get("/api/customers/johndoe", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["username"] == "johndoe"

def test_charge_customer(setup_customer):
    """
    Test charging the customer's wallet.

    - Uses LineProfiler to measure performance of `charge_wallet`.
    - Asserts that the wallet balance is updated correctly.
    """
    lp = LineProfiler()
    lp.add_function(CustomerService.charge_wallet)

    @lp
    def execute():
        response = client.post(
    "/api/customers/johndoe/charge",
    json={"amount": 100.0},
    headers=HEADERS,
)
        assert response.status_code == 200
        assert response.json()["customer"]["wallet_balance"] == 100.0

    execute()
    lp.print_stats()

def test_deduct_customer(setup_customer):
    """
    Test deducting from the customer's wallet.

    - Uses LineProfiler to measure performance of `deduct_wallet`.
    - Asserts that the wallet balance decreases correctly.
    """
    lp = LineProfiler()
    lp.add_function(CustomerService.deduct_wallet)

    @lp
    def execute():
        response = client.post(
            "/api/customers/johndoe/deduct",
            json={"amount": 50.0},
            headers=HEADERS,
        )
        assert response.status_code == 200
        assert response.json()["customer"]["wallet_balance"] == 50.0

    execute()
    lp.print_stats()

def test_delete_customer(setup_customer):
    """
    Test deleting a customer by username.

    - Uses LineProfiler to measure performance of `delete_customer`.
    - Verifies that the customer no longer exists after deletion.
    """
    lp = LineProfiler()
    lp.add_function(CustomerService.delete_customer)

    @lp
    def execute():
        response = client.delete("/api/customers/johndoe", headers=HEADERS)
        assert response.status_code == 200
        assert response.json()["message"] == "Customer deleted successfully"

        # Verify the customer is deleted
        response = client.get("/api/customers/johndoe", headers=HEADERS)
        assert response.status_code == 404
        assert response.json()["detail"] == "Customer not found"

    execute()
    lp.print_stats()
