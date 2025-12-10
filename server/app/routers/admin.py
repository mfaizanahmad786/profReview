"""Admin Routes - Administrative functions for moderating content"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.review import Review
from app.models.review_flag import ReviewFlag
from app.models.professor import Professor
from app.schemas.review import ReviewResponse

router = APIRouter(prefix="/admin", tags=["Admin"])


def require_admin(current_user: User = Depends(get_current_user)):
    """Dependency to ensure user is an admin"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


@router.get("/flagged-reviews", response_model=List[dict])
async def get_flagged_reviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Get all flagged reviews with details.
    Only accessible by admins.
    Returns reviews with flag count and reasons.
    """
    # Get all flagged reviews
    flagged_reviews = db.query(Review).filter(
        Review.is_flagged == True
    ).order_by(Review.flag_count.desc()).all()
    
    result = []
    for review in flagged_reviews:
        # Get flags for this review
        flags = db.query(ReviewFlag).filter(
            ReviewFlag.review_id == review.id
        ).all()
        
        # Get professor name
        professor = db.query(Professor).filter(
            Professor.id == review.professor_id
        ).first()
        
        # Get student info
        student = db.query(User).filter(
            User.id == review.student_id
        ).first()
        
        flag_details = [
            {
                "user_id": flag.user_id,
                "reason": flag.reason,
                "flagged_at": flag.flagged_at
            }
            for flag in flags
        ]
        
        result.append({
            "id": review.id,
            "professor_id": review.professor_id,
            "professor_name": professor.name if professor else "Unknown",
            "student_id": review.student_id,
            "student_email": student.email if student else "Unknown",
            "rating_quality": review.rating_quality,
            "rating_difficulty": review.rating_difficulty,
            "grade_received": review.grade_received.value,
            "comment": review.comment,
            "course_code": review.course_code,
            "semester": review.semester,
            "created_at": review.created_at,
            "flag_count": review.flag_count,
            "flags": flag_details
        })
    
    return result


@router.delete("/reviews/{review_id}", status_code=status.HTTP_200_OK)
async def delete_flagged_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Permanently delete a review.
    Only accessible by admins.
    Use this when the review violates community guidelines.
    """
    review = db.query(Review).filter(Review.id == review_id).first()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    professor_id = review.professor_id
    
    # Delete the review (flags will be cascade deleted)
    db.delete(review)
    db.commit()
    
    # Update professor stats
    _update_professor_stats(db, professor_id)
    
    return {
        "message": "Review deleted successfully",
        "review_id": review_id
    }


@router.post("/reviews/{review_id}/dismiss-flags", status_code=status.HTTP_200_OK)
async def dismiss_flags(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Dismiss all flags on a review without deleting it.
    Only accessible by admins.
    Use this when the review is acceptable despite flags.
    """
    review = db.query(Review).filter(Review.id == review_id).first()
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    # Delete all flags for this review
    db.query(ReviewFlag).filter(ReviewFlag.review_id == review_id).delete()
    
    # Update review flag status
    review.is_flagged = False
    review.flag_count = 0
    
    db.commit()
    
    return {
        "message": "Flags dismissed successfully",
        "review_id": review_id
    }


def _update_professor_stats(db: Session, professor_id: int):
    """Helper function to recalculate professor statistics"""
    from app.models.professor import Professor
    
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    if not professor:
        return
    
    # Get all visible reviews for this professor
    reviews = db.query(Review).filter(
        Review.professor_id == professor_id,
        Review.is_hidden == 0
    ).all()
    
    if not reviews:
        professor.average_rating = 0.0
        professor.average_difficulty = 0.0
        professor.total_reviews = 0
    else:
        professor.average_rating = sum(r.rating_quality for r in reviews) / len(reviews)
        professor.average_difficulty = sum(r.rating_difficulty for r in reviews) / len(reviews)
        professor.total_reviews = len(reviews)
    
    db.commit()
