from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.review_service import ReviewService
from database import get_db

router = APIRouter()
review_service = ReviewService()

@router.post("/reviews")
def submit_review(data: dict, db: Session = Depends(get_db)):
    try:
        new_review = review_service.submit_review(db, data)
        return {"message": "Review submitted successfully", "review": new_review}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/reviews/{review_id}")
def update_review(review_id: int, updates: dict, db: Session = Depends(get_db)):
    try:
        updated_review = review_service.update_review(db, review_id, updates)
        return {"message": "Review updated successfully", "review": updated_review}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    try:
        review_service.delete_review(db, review_id)
        return {"message": "Review deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/reviews/product/{product_id}")
def get_product_reviews(product_id: int, db: Session = Depends(get_db)):
    reviews = review_service.get_product_reviews(db, product_id)
    return reviews

@router.get("/reviews/customer/{customer_id}")
def get_customer_reviews(customer_id: int, db: Session = Depends(get_db)):
    reviews = review_service.get_customer_reviews(db, customer_id)
    return reviews

@router.post("/reviews/{review_id}/moderate")
def moderate_review(review_id: int, status: str, db: Session = Depends(get_db)):
    try:
        moderated_review = review_service.moderate_review(db, review_id, status)
        return {"message": "Review moderation updated", "review": moderated_review}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
