from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.review_service import ReviewService
from database import get_db
from dependencies.auth_dependency import get_current_user, require_admin
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()
review_service = ReviewService()

@router.post("/reviews", dependencies=[Depends(get_current_user), Depends(limiter.limit("10/minute"))])
def submit_review(data: dict, db: Session = Depends(get_db)):
    try:
        new_review = review_service.submit_review(db, data)
        return {"message": "Review submitted successfully", "review": new_review}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.put("/reviews/{review_id}", dependencies=[Depends(get_current_user),Depends(limiter.limit("10/minute"))])
def update_review(review_id: int, updates: dict, db: Session = Depends(get_db)):
    try:
        updated_review = review_service.update_review(db, review_id, updates)
        return {"message": "Review updated successfully", "review": updated_review}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.delete("/reviews/{review_id}", dependencies=[Depends(get_current_user), Depends(limiter.limit("10/minute"))])
def delete_review(review_id: int, db: Session = Depends(get_db)):
    try:
        review_service.delete_review(db, review_id)
        return {"message": "Review deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/reviews/product/{product_id}", dependencies=[Depends(get_current_user), Depends(limiter.limit("10/minute"))])
def get_product_reviews(product_id: int, db: Session = Depends(get_db)):
    reviews = review_service.get_product_reviews(db, product_id)
    return reviews

@router.get("/reviews/customer/{customer_id}", dependencies=[Depends(get_current_user), Depends(limiter.limit("10/minute"))])
def get_customer_reviews(customer_id: int, db: Session = Depends(get_db)):
    reviews = review_service.get_customer_reviews(db, customer_id)
    return reviews

class ReviewModerationRequest(BaseModel):
    status: str

@router.put("/reviews/{review_id}/moderate", dependencies=[Depends(require_admin), Depends(limiter.limit("10/minute"))])
def moderate_review_route(review_id: int, request: ReviewModerationRequest, db: Session = Depends(get_db)):
    """Moderate a review by approving or rejecting it."""
    try:
        return review_service.moderate_review(db, review_id, request.status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/reviews/pending", dependencies=[Depends(require_admin), Depends(limiter.limit("10/minute"))])
def get_pending_reviews_route(db: Session = Depends(get_db)):
    """Fetch all reviews pending moderation."""
    try:
        return review_service.get_pending_reviews(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))