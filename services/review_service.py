from sqlalchemy.orm import Session
from models.review import Review
from memory_profiler import profile

class ReviewService:
    @profile
    def submit_review(self, db: Session, data: dict):
        new_review = Review(
            product_id=data["product_id"],
            customer_id=data["customer_id"],
            rating=data["rating"],
            comment=data.get("comment", ""),
        )
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return new_review

    @profile
    def update_review(self, db: Session, review_id: int, updates: dict):
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise ValueError("Review not found")

        for key, value in updates.items():
            setattr(review, key, value)
        db.commit()
        db.refresh(review)
        return review

    @profile
    def delete_review(self, db: Session, review_id: int):
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise ValueError("Review not found")

        db.delete(review)
        db.commit()

    @profile
    def get_product_reviews(self, db: Session, product_id: int):
        return db.query(Review).filter(Review.product_id == product_id).all()

    @profile
    def get_customer_reviews(self, db: Session, customer_id: int):
        return db.query(Review).filter(Review.customer_id == customer_id).all()

    @profile
    def moderate_review(self, db: Session, review_id: int, status: str):
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise ValueError("Review not found")

        review.moderated = status  # Set to Approved or Rejected
        db.commit()
        db.refresh(review)
        return review
