import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi.testclient import TestClient
from line_profiler import LineProfiler

from app_review import app
from services.review_service import ReviewService

client = TestClient(app)
service = ReviewService()

def test_submit_review():
    lp = LineProfiler()
    lp.add_function(service.submit_review.__wrapped__)  # Profile wrapped function

    @lp
    def execute():
        response = client.post("/api/reviews", json={
            "product_id": 1,
            "customer_id": 1,
            "rating": 4.5,
            "comment": "Excellent product!"
        })
        assert response.status_code == 200
        assert response.json()["review"]["rating"] == 4.5

    execute()
    lp.print_stats()

def test_get_product_reviews():
    response = client.get("/api/reviews/product/1")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_customer_reviews():
    response = client.get("/api/reviews/customer/1")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_review():
    lp = LineProfiler()
    lp.add_function(service.update_review.__wrapped__)  # Profile wrapped function

    @lp
    def execute():
        response = client.put("/api/reviews/1", json={
            "rating": 5.0,
            "comment": "Updated review: Perfect!"
        })
        assert response.status_code == 200
        assert response.json()["review"]["rating"] == 5.0

    execute()
    lp.print_stats()

def test_moderate_review():
    lp = LineProfiler()
    lp.add_function(service.moderate_review.__wrapped__)  # Profile wrapped function

    @lp
    def execute():
        response = client.post("/api/reviews/1/moderate?status=Approved")
        assert response.status_code == 200
        assert response.json()["review"]["moderated"] == "Approved"

    execute()
    lp.print_stats()

def test_delete_review():
    lp = LineProfiler()
    lp.add_function(service.delete_review.__wrapped__)  # Profile wrapped function

    @lp
    def execute():
        response = client.delete("/api/reviews/1")
        assert response.status_code == 200

    execute()
    lp.print_stats()
