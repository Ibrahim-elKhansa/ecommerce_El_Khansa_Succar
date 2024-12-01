import sys
import os
from fastapi.testclient import TestClient
from fastapi import FastAPI
from routes.review_routes import router as review_router

app = FastAPI()
app.include_router(review_router, prefix="/api")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = TestClient(app)


def test_submit_review():
    """
    Test submitting a review.
    """
    data = {
        "product_id": 1,
        "customer_id": 2,
        "rating": 5,
        "comment": "Great product!"
    }
    response = client.post("/api/reviews", json=data)
    assert response.status_code == 200
    assert response.json()["review"]["product_id"] == 1
    assert response.json()["review"]["customer_id"] == 2
    assert response.json()["review"]["rating"] == 5
    assert response.json()["review"]["comment"] == "Great product!"


def test_get_product_reviews():
    """
    Test retrieving reviews for a product.
    """
    product_id = 1
    response = client.get(f"/api/reviews/product/{product_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_customer_reviews():
    """
    Test retrieving reviews by a customer.
    """
    customer_id = 2
    response = client.get(f"/api/reviews/customer/{customer_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_review():
    """
    Test updating a review.
    """
    review_id = 1 
    updates = {
        "rating": 4,
        "comment": "Updated comment"
    }
    response = client.put(f"/api/reviews/{review_id}", json=updates)
    assert response.status_code == 200
    assert response.json()["review"]["rating"] == 4
    assert response.json()["review"]["comment"] == "Updated comment"


def test_moderate_review():
    """
    Test moderating a review.
    """
    review_id = 1 
    moderation_data = {"status": "Approved"}
    response = client.put(f"/api/reviews/{review_id}/moderate", json=moderation_data)
    assert response.status_code == 200
    assert response.json()["review"]["moderation_status"] == "Approved"


def test_get_pending_reviews():
    """
    Test retrieving pending reviews.
    """
    response = client.get("/api/reviews/pending")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_review():
    """
    Test deleting a review.
    """
    review_id = 1 
    response = client.delete(f"/api/reviews/{review_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Review deleted successfully"

    response = client.get(f"/api/reviews/product/1")
    assert response.status_code == 200
    assert not any(review["id"] == review_id for review in response.json())