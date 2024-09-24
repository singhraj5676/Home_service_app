#review_routes.py
import uuid
from typing import List
from database import get_db
from utils.helper_func import *
from models.review import Review
from sqlalchemy.orm import Session
from fastapi import APIRouter, Query
from models.user_models import UserInDB
from fastapi import Depends, HTTPException
from schemas.auth_models  import ReviewCreate, ReviewUpdate
from response.review_response import ReviewResponse, ReviewGetResponse


router = APIRouter()


@router.post("/", response_model=ReviewResponse)
def add_review(review_data: ReviewCreate, db: Session = Depends(get_db)):
    # Check if the author and receiver exist
    author = db.query(UserInDB).filter(UserInDB.id == review_data.author_id).first()
    receiver = db.query(UserInDB).filter(UserInDB.id == review_data.receiver_id).first()

    if not author or not receiver:
        raise HTTPException(status_code=404, detail="Author or receiver not found")
    
    # Check if a review already exists from this author to this receiver
    existing_review = db.query(Review).filter(
        Review.author_id == review_data.author_id,
        Review.receiver_id == review_data.receiver_id
    ).first()

    if existing_review:
        raise HTTPException(status_code=400, detail="Review already exists")

    # Create a new review instance
    new_review = Review(
        score=review_data.score,
        text=review_data.text,
        author_id=review_data.author_id,
        receiver_id=review_data.receiver_id
    )

    # Add the new review to the session and commit the transaction
    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    # Return the newly created review using the response schema
    return new_review


@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: uuid.UUID, review_data: ReviewUpdate, db: Session = Depends(get_db)):
    # Check if the review exists
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if review_data.score is not None:
        review.score = review_data.score
    if review_data.text is not None:
        review.text = review_data.text

    # Commit the transaction
    db.commit()
    db.refresh(review)

    # Return the updated review using the response schema
    return review

@router.get("/{review_id}", response_model=ReviewGetResponse)
def get_review(review_id: uuid.UUID, db: Session = Depends(get_db)):
    print(review_id)

    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return review


@router.get("/reviews/by-receiver", response_model=List[ReviewGetResponse])
def get_reviews_by_author(
    receiver_id: uuid.UUID = Query(..., description="The UUID of the author"),
    db: Session = Depends(get_db)
):
    # This print statement helps to debug if the UUID is being parsed
    print("Received author_id:", receiver_id)

    # Query for reviews by the author
    receiver_reviews = db.query(Review).filter(Review.receiver_id == receiver_id).all()

    if not receiver_reviews:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return receiver_reviews

@router.get("/reviews/by-author", response_model=List[ReviewGetResponse])
def get_reviews_by_author(
    author_id: uuid.UUID = Query(..., description="The UUID of the author"),
    db: Session = Depends(get_db)
):
    # This print statement helps to debug if the UUID is being parsed
    print("Received author_id:", author_id)

    # Query for reviews by the author
    author_reviews = db.query(Review).filter(Review.author_id == author_id).all()

    if not author_reviews:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return author_reviews
