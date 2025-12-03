"""Review Routes - CRUD operations for student reviews"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.models.user import User
from app.models.professor import Professor
from app.models.review import Review, GradeEnum
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse


router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new review for a professor.
    - Requires authentication
    - One review per professor per semester per student
    """
    # Check if professor exists
    professor = db.query(Professor).filter(Professor.id == review_data.professor_id).first()
    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor not found"
        )
    
    # Check if user already reviewed this professor this semester
    existing_review = db.query(Review).filter(
        Review.professor_id == review_data.professor_id,
        Review.student_id == current_user.id,
        Review.semester == review_data.semester
    ).first()
    
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this professor for this semester"
        )
    
    # Create the review
    new_review = Review(
        professor_id=review_data.professor_id,
        student_id=current_user.id,
        rating_quality=review_data.rating_quality,
        rating_difficulty=review_data.rating_difficulty,
        grade_received=review_data.grade_received,
        comment=review_data.comment,
        course_code=review_data.course_code,
        semester=review_data.semester
    )
    
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    
    # Update professor's aggregate stats
    _update_professor_stats(db, review_data.professor_id)
    
    return new_review


@router.get("/professor/{professor_id}", response_model=List[ReviewResponse])
def get_professor_reviews(
    professor_id: int,
    db: Session = Depends(get_db)
):
    """Get all reviews for a specific professor"""
    # Check if professor exists
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor not found"
        )
    
    reviews = db.query(Review).filter(
        Review.professor_id == professor_id,
        Review.is_hidden == 0
    ).order_by(Review.created_at.desc()).all()
    
    return reviews


@router.get("/me", response_model=List[ReviewResponse])
def get_my_reviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all reviews by the current logged-in user"""
    reviews = db.query(Review).filter(
        Review.student_id == current_user.id
    ).order_by(Review.created_at.desc()).all()
    
    return reviews


@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    """Get a specific review by ID"""
    review = db.query(Review).filter(Review.id == review_id).first()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    return review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a review (only owner or admin can delete)"""
    review = db.query(Review).filter(Review.id == review_id).first()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    # Check if user owns the review or is admin
    if review.student_id != current_user.id and not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this review"
        )
    
    professor_id = review.professor_id
    db.delete(review)
    db.commit()
    
    # Update professor stats after deletion
    _update_professor_stats(db, professor_id)
    
    return None


@router.get("/professor/{professor_id}/grade-distribution")
def get_grade_distribution(professor_id: int, db: Session = Depends(get_db)):
    """
    Get grade distribution for a professor.
    This is the KEY endpoint for your Grade Distribution Chart!
    Returns: [{"grade": "A", "count": 15}, {"grade": "B", "count": 8}, ...]
    """
    # Check if professor exists
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor not found"
        )
    
    # Aggregate grades using SQL GROUP BY
    results = db.query(
        Review.grade_received,
        func.count(Review.id).label('count')
    ).filter(
        Review.professor_id == professor_id,
        Review.is_hidden == 0
    ).group_by(
        Review.grade_received
    ).all()
    
    # Convert to format Recharts expects
    chart_data = [{"grade": r.grade_received.value, "count": r.count} for r in results]
    
    # Sort by grade order (A+ first, F last)
    grade_order = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F", "W"]
    chart_data.sort(key=lambda x: grade_order.index(x["grade"]) if x["grade"] in grade_order else 99)
    
    return chart_data


def _update_professor_stats(db: Session, professor_id: int):
    """
    Helper function to update a professor's aggregate stats.
    Called after creating or deleting a review.
    """
    # Get all non-hidden reviews for this professor
    reviews = db.query(Review).filter(
        Review.professor_id == professor_id,
        Review.is_hidden == 0
    ).all()
    
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    
    if reviews:
        # Calculate averages
        professor.avg_rating = sum(r.rating_quality for r in reviews) / len(reviews)
        professor.avg_difficulty = sum(r.rating_difficulty for r in reviews) / len(reviews)
        professor.total_reviews = len(reviews)
    else:
        # No reviews - reset to defaults
        professor.avg_rating = 0.0
        professor.avg_difficulty = 0.0
        professor.total_reviews = 0
    
    db.commit()

