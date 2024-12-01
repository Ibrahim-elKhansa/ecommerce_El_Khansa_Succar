import sys
import os
from decouple import config
from fastapi.testclient import TestClient
from line_profiler import LineProfiler

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app_review.app_review import app
from services.review_service import ReviewService

client = TestClient(app)
service = ReviewService()

# Load the admin token from .env
ADMIN_TOKEN = config("ADMIN_TOKEN")

# Add the Authorization header for all requests
HEADERS = {"Authorization": f"Bearer {ADMIN_TOKEN}"}

def test_submit_review():
    """
    Test submitting a review.

    - Profiles the `submit_review` method to evaluate performance.
    - Verifies that the review is successfully created.
    - Ensures the response contains the expected review details.
    """
    lp = LineProfiler()
    lp.add_function(service.submit_review.__wrapped__)  # Profile wrapped function

    @lp
    def execute():
        response = client.post(
            "/api/reviews",
            json={
                "product_id": 1,
                "customer_id": 1,
                "rating": 4.5,
                "comment": "Excellent product!",
            },
            headers=HEADERS,
        )
        assert response.status_code == 200
        assert response.json()["review"]["rating"] == 4.5

    execute()
    lp.print_stats()

def test_get_product_reviews():
    """
    Test retrieving reviews for a specific product.

    - Ensures that the API returns a list of reviews for the specified product.
    - Verifies that the list contains at least one review.
    """
    response = client.get("/api/reviews/product/1", headers=HEADERS)
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_customer_reviews():
    """
    Test retrieving reviews by a specific customer.

    - Ensures that the API returns a list of reviews submitted by the specified customer.
    - Verifies that the list contains at least one review.
    """
    response = client.get("/api/reviews/customer/1", headers=HEADERS)
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_review():
    """
    Test updating an existing review.

    - Profiles the `update_review` method to evaluate performance.
    - Updates the review's rating and comment.
    - Verifies that the API reflects the updated review details.
    """
    lp = LineProfiler()
    lp.add_function(service.update_review.__wrapped__)

    @lp
    def execute():
        response = client.put(
            "/api/reviews/1",
            json={
                "rating": 5.0,
                "comment": "Updated review: Perfect!",
            },
            headers=HEADERS,
        )
        assert response.status_code == 200
        assert response.json()["review"]["rating"] == 5.0

    execute()
    lp.print_stats()

def test_moderate_review():
    """
    Test moderating a review (approve/reject).

    - Profiles the `moderate_review` method to evaluate performance.
    - Moderates the review to 'Approved' status.
    - Verifies that the moderation status is updated correctly in the response.
    """
    lp = LineProfiler()
    lp.add_function(service.moderate_review.__wrapped__)

    @lp
    def execute():
        response = client.put(
            "/api/reviews/1/moderate",
            json={"status": "Approved"},
            headers=HEADERS,
        )
        print(response.json())
        assert response.status_code == 200
        print(response.json())
        assert response.json()["review"]["moderation_status"] == "Approved"

    execute()
    lp.print_stats()


def test_delete_review():
    """
    Test deleting a review.

    - Profiles the `delete_review` method to evaluate performance.
    - Deletes a specific review by ID.
    - Verifies that the review is deleted successfully.
    """
    lp = LineProfiler()
    lp.add_function(service.delete_review.__wrapped__)  # Profile wrapped function

    @lp
    def execute():
        response = client.delete("/api/reviews/1", headers=HEADERS)
        assert response.status_code == 200

    execute()
    lp.print_stats()
