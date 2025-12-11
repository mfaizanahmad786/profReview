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
from app.models.professor_claim_request import ProfessorClaimRequest, ClaimStatus
from app.schemas.review import ReviewResponse
from app.schemas.professor_claim import ClaimRequestResponse

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


@router.get("/claim-requests", response_model=List[dict])
async def get_pending_claim_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Get all pending professor claim requests.
    Only accessible by admins.
    """
    pending_claims = db.query(ProfessorClaimRequest).filter(
        ProfessorClaimRequest.status == ClaimStatus.PENDING
    ).order_by(ProfessorClaimRequest.requested_at.desc()).all()
    
    result = []
    for claim in pending_claims:
        # Get professor info
        professor = db.query(Professor).filter(Professor.id == claim.professor_id).first()
        
        # Get user info
        user = db.query(User).filter(User.id == claim.user_id).first()
        
        result.append({
            "id": claim.id,
            "user_id": claim.user_id,
            "user_email": user.email if user else "Unknown",
            "professor_id": claim.professor_id,
            "professor_name": professor.name if professor else "Unknown",
            "professor_department": professor.department if professor else "Unknown",
            "request_message": claim.request_message,
            "status": claim.status.value,
            "requested_at": claim.requested_at,
            "reviewed_at": claim.reviewed_at
        })
    
    return result


@router.post("/claim-requests/{claim_id}/approve", status_code=status.HTTP_200_OK)
async def approve_claim_request(
    claim_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Approve a professor claim request.
    Only accessible by admins.
    """
    claim = db.query(ProfessorClaimRequest).filter(
        ProfessorClaimRequest.id == claim_id
    ).first()
    
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim request not found"
        )
    
    if claim.status != ClaimStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot approve claim with status: {claim.status.value}"
        )
    
    # Check if professor is already claimed by another user
    existing_claim = db.query(ProfessorClaimRequest).filter(
        ProfessorClaimRequest.professor_id == claim.professor_id,
        ProfessorClaimRequest.status == ClaimStatus.APPROVED,
        ProfessorClaimRequest.id != claim_id
    ).first()
    
    if existing_claim:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This professor profile is already claimed by another user"
        )
    
    # Approve the claim
    claim.approve(current_user.id)
    
    # Update professor's claimed_by_user_id field
    professor = db.query(Professor).filter(Professor.id == claim.professor_id).first()
    if professor:
        professor.claimed_by_user_id = claim.user_id
        professor.is_claimed = True
        professor.claimed_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "message": "Claim request approved successfully",
        "claim_id": claim_id,
        "professor_id": claim.professor_id,
        "user_id": claim.user_id
    }


@router.post("/claim-requests/{claim_id}/reject", status_code=status.HTTP_200_OK)
async def reject_claim_request(
    claim_id: int,
    admin_comment: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Reject a professor claim request.
    Only accessible by admins.
    """
    claim = db.query(ProfessorClaimRequest).filter(
        ProfessorClaimRequest.id == claim_id
    ).first()
    
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim request not found"
        )
    
    if claim.status != ClaimStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot reject claim with status: {claim.status.value}"
        )
    
    # Reject the claim
    claim.reject(current_user.id, admin_comment)
    db.commit()
    
    return {
        "message": "Claim request rejected",
        "claim_id": claim_id,
        "admin_comment": admin_comment
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
