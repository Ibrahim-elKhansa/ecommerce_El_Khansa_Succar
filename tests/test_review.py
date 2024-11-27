import pytest
from fastapi.testclient import TestClient
from app_review import app

client = TestClient(app)

def test_submit_review():
    response = client.post("/api/reviews", json={
        "product_id": 1,  # Assuming product ID = 1 exists
        "customer_id": 1,  # Assuming customer ID = 1 exists
        "rating": 4.5,
        "comment": "Excellent product!"
    })
    assert response.status_code == 200
    assert response.json()["review"]["rating"] == 4.5

def test_get_product_reviews():
    response = client.get("/api/reviews/product/1")  # Assuming product ID = 1
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_customer_reviews():
    response = client.get("/api/reviews/customer/1")  # Assuming customer ID = 1
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_review():
    response = client.put("/api/reviews/1", json={  # Assuming review ID = 1
        "rating": 5.0,
        "comment": "Updated review: Perfect!"
    })
    assert response.status_code == 200
    assert response.json()["review"]["rating"] == 5.0

def test_moderate_review():
    response = client.post("/api/reviews/1/moderate", json={  # Assuming review ID = 1
        "status": "Approved"
    })
    assert response.status_code == 200
    assert response.json()["review"]["moderated"] == "Approved"

def test_delete_review():
    response = client.delete("/api/reviews/1")  # Assuming review ID = 1
    assert response.status_code == 200
