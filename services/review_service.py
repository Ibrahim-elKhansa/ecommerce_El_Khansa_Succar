from sqlalchemy.orm import Session
from models.review import Review
from memory_profiler import profile
from bleach import clean

class ReviewService:
    def validate_review_data(self, data: dict):
        # Ensure rating is between 1 and 5
        if not 1 <= data.get("rating", 0) <= 5:
            raise ValueError("Rating must be between 1 and 5.")
        
        # Ensure comment is not empty and has a valid length
        comment = data.get("comment", "").strip()
        if len(comment) > 500:
            raise ValueError("Comment cannot exceed 500 characters.")
        
        # Sanitize the comment to prevent XSS attacks
        data["comment"] = clean(comment, strip=True)
        return data

    @profile
    def submit_review(self, db: Session, data: dict):
        # Validate and sanitize data
        validated_data = self.validate_review_data(data)

        new_review = Review(
            product_id=validated_data["product_id"],
            customer_id=validated_data["customer_id"],
            rating=validated_data["rating"],
            comment=validated_data.get("comment", ""),
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

        # Validate and sanitize updates
        if "rating" in updates or "comment" in updates:
            updates = self.validate_review_data(updates)

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
        """Moderate a review: Approve or Reject."""
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise ValueError("Review not found")
        if status not in ["Approved", "Rejected"]:
            raise ValueError("Invalid moderation status")
        review.moderation_status = status
        db.commit()
        db.refresh(review)
        return review

    @profile
    def get_pending_reviews(self, db: Session):
        """Fetch reviews that are pending moderation."""
        return db.query(Review).filter(Review.moderation_status == "Pending").all()
    
if __name__ == "__main__":
    from database import SessionLocal

    # Initialize database session and service
    db = SessionLocal()
    service = ReviewService()

    @profile
    def test_review_service():
        # Submitting a review
        print("Submitting a review...")
        created_review = service.submit_review(db, {
            "product_id": 1,
            "customer_id": 2,
            "rating": 5,
            "comment": "Great product!"
        })
        print(f"Created review: {created_review}")

        # Fetch product reviews
        print("Fetching product reviews...")
        print(service.get_product_reviews(db, 1))

        # Fetch customer reviews
        print("Fetching customer reviews...")
        print(service.get_customer_reviews(db, 2))

        # Update review
        print("Updating review...")
        print(service.update_review(db, created_review.id, {
            "rating": 4,
            "comment": "Updated comment"
        }))

        # Moderate review
        print("Moderating review...")
        print(service.moderate_review(db, created_review.id, "Approved"))

        # Delete review
        print("Deleting review...")
        service.delete_review(db, created_review.id)
        print(f"Deleted review ID: {created_review.id}")

    test_review_service()
    db.close()
