import os
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.review_service import ReviewService
from database import get_db
from dependencies.auth_dependency import get_current_user, require_admin
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address

# Set up logging
os.makedirs("logs", exist_ok=True)  # Ensure logs directory exists
logging.basicConfig(
    filename="logs/log_review.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()
review_service = ReviewService()

@router.post("/reviews", dependencies=[Depends(get_current_user)])
def submit_review(data: dict, db: Session = Depends(get_db)):
    logging.info(f"POST /reviews - Data: {data}")
    try:
        new_review = review_service.submit_review(db, data)
        logging.info(f"Review submitted: {new_review}")
        return {"message": "Review submitted successfully", "review": new_review}
    except ValueError as e:
        logging.error(f"Error submitting review: {e}")
        raise HTTPException(status_code=422, detail=str(e))

@router.put("/reviews/{review_id}", dependencies=[Depends(get_current_user)])
def update_review(review_id: int, updates: dict, db: Session = Depends(get_db)):
    logging.info(f"PUT /reviews/{review_id} - Updates: {updates}")
    try:
        updated_review = review_service.update_review(db, review_id, updates)
        logging.info(f"Review updated: {updated_review}")
        return {"message": "Review updated successfully", "review": updated_review}
    except ValueError as e:
        logging.error(f"Error updating review {review_id}: {e}")
        raise HTTPException(status_code=422, detail=str(e))

@router.delete("/reviews/{review_id}", dependencies=[Depends(get_current_user)])
def delete_review(review_id: int, db: Session = Depends(get_db)):
    logging.info(f"DELETE /reviews/{review_id}")
    try:
        review_service.delete_review(db, review_id)
        logging.info(f"Review deleted: {review_id}")
        return {"message": "Review deleted successfully"}
    except ValueError as e:
        logging.error(f"Error deleting review {review_id}: {e}")
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/reviews/product/{product_id}", dependencies=[Depends(get_current_user)])
def get_product_reviews(product_id: int, db: Session = Depends(get_db)):
    logging.info(f"GET /reviews/product/{product_id}")
    reviews = review_service.get_product_reviews(db, product_id)
    logging.info(f"Product reviews retrieved for product_id={product_id}: {len(reviews)} reviews")
    return reviews

@router.get("/reviews/customer/{customer_id}", dependencies=[Depends(get_current_user)])
def get_customer_reviews(customer_id: int, db: Session = Depends(get_db)):
    logging.info(f"GET /reviews/customer/{customer_id}")
    reviews = review_service.get_customer_reviews(db, customer_id)
    logging.info(f"Customer reviews retrieved for customer_id={customer_id}: {len(reviews)} reviews")
    return reviews

class ReviewModerationRequest(BaseModel):
    status: str

@router.put("/reviews/{review_id}/moderate", dependencies=[Depends(require_admin)])
def moderate_review_route(review_id: int, request: ReviewModerationRequest, db: Session = Depends(get_db)):
    logging.info(f"PUT /reviews/{review_id}/moderate - Status: {request.status}")
    try:
        result = review_service.moderate_review(db, review_id, request.status)
        logging.info(f"Review moderated: {result}")
        return {"message": "Review moderated successfully", "review": result}
    except ValueError as e:
        logging.error(f"Error moderating review {review_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reviews/pending", dependencies=[Depends(require_admin)])
def get_pending_reviews_route(db: Session = Depends(get_db)):
    logging.info("GET /reviews/pending")
    try:
        pending_reviews = review_service.get_pending_reviews(db)
        logging.info(f"Pending reviews retrieved: {len(pending_reviews)} reviews")
        return pending_reviews
    except Exception as e:
        logging.error(f"Error fetching pending reviews: {e}")
        raise HTTPException(status_code=400, detail=str(e))
