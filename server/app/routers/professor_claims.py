"""Professor Claim Routes - Handle professor profile claiming"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Optional
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.professor import Professor
from app.models.professor_claim_request import ProfessorClaimRequest, ClaimStatus
from app.schemas.professor_claim import (
    ClaimRequestCreate,
    ClaimRequestResponse,
    ClaimStatusResponse
)


router = APIRouter(prefix="/professors", tags=["Professor Claims"])


@router.post("/{professor_id}/claim-request", response_model=ClaimRequestResponse, status_code=status.HTTP_201_CREATED)
async def submit_claim_request(
    professor_id: int,
    claim_data: ClaimRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit a claim request for a professor profile.
    - Only users with PROFESSOR role can claim
    - Professor profile must exist
    - Professor profile must not be already claimed
    - User can only have one active claim (pending or approved)
    """
    # Check if user is a professor
    if current_user.role != UserRole.PROFESSOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only professors can claim profiles"
        )
    
    # Check if professor exists
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor not found"
        )
    
    # Check if professor is already claimed
    if professor.is_claimed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This professor profile has already been claimed"
        )
    
    # Check if user already has an approved claim
    existing_approved = db.query(ProfessorClaimRequest).filter(
        ProfessorClaimRequest.user_id == current_user.id,
        ProfessorClaimRequest.status == ClaimStatus.APPROVED
    ).first()
    
    if existing_approved:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already claimed a professor profile"
        )
    
    # Check if user already has a pending claim for this professor
    existing_pending = db.query(ProfessorClaimRequest).filter(
        ProfessorClaimRequest.user_id == current_user.id,
        ProfessorClaimRequest.professor_id == professor_id,
        ProfessorClaimRequest.status == ClaimStatus.PENDING
    ).first()
    
    if existing_pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a pending claim request for this professor"
        )
    
    # Create the claim request
    new_claim = ProfessorClaimRequest(
        user_id=current_user.id,
        professor_id=professor_id,
        request_message=claim_data.request_message,
        status=ClaimStatus.PENDING
    )
    
    db.add(new_claim)
    db.commit()
    db.refresh(new_claim)
    
    return new_claim


@router.get("/my-claim-status", response_model=ClaimStatusResponse)
async def get_my_claim_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get the current user's claim status.
    Returns information about pending, approved, or rejected claims.
    """
    # Check for pending claim
    pending_claim = db.query(ProfessorClaimRequest).filter(
        ProfessorClaimRequest.user_id == current_user.id,
        ProfessorClaimRequest.status == ClaimStatus.PENDING
    ).first()
    
    # Check for approved claim
    approved_claim = db.query(ProfessorClaimRequest).filter(
        ProfessorClaimRequest.user_id == current_user.id,
        ProfessorClaimRequest.status == ClaimStatus.APPROVED
    ).first()
    
    # Check for rejected claim (most recent)
    rejected_claim = db.query(ProfessorClaimRequest).filter(
        ProfessorClaimRequest.user_id == current_user.id,
        ProfessorClaimRequest.status == ClaimStatus.REJECTED
    ).order_by(ProfessorClaimRequest.reviewed_at.desc()).first()
    
    # Get the most relevant claim to return
    claim_to_return = pending_claim or approved_claim or rejected_claim
    
    return ClaimStatusResponse(
        has_pending=pending_claim is not None,
        has_approved=approved_claim is not None,
        has_rejected=rejected_claim is not None,
        claim_request=claim_to_return,
        claimed_professor_id=approved_claim.professor_id if approved_claim else None
    )


@router.get("/my-claimed-profile")
async def get_my_claimed_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get the professor profile that the current user has claimed (if approved).
    Returns 404 if no approved claim exists.
    """
    # Find approved claim
    approved_claim = db.query(ProfessorClaimRequest).filter(
        ProfessorClaimRequest.user_id == current_user.id,
        ProfessorClaimRequest.status == ClaimStatus.APPROVED
    ).first()
    
    if not approved_claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No approved claim found"
        )
    
    # Get the professor profile
    professor = db.query(Professor).filter(Professor.id == approved_claim.professor_id).first()
    
    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor profile not found"
        )
    
    return {
        "id": professor.id,
        "name": professor.name,
        "department": professor.department,
        "avg_rating": professor.avg_rating,
        "avg_difficulty": professor.avg_difficulty,
        "total_reviews": professor.total_reviews,
        "is_claimed": professor.is_claimed,
        "claimed_at": professor.claimed_at
    }


@router.delete("/claim-request/{claim_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_claim_request(
    claim_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cancel a pending claim request.
    Only the owner can cancel, and only if status is PENDING.
    """
    claim = db.query(ProfessorClaimRequest).filter(
        ProfessorClaimRequest.id == claim_id
    ).first()
    
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim request not found"
        )
    
    # Check ownership
    if claim.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel this claim request"
        )
    
    # Check if still pending
    if claim.status != ClaimStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only cancel pending claim requests"
        )
    
    db.delete(claim)
    db.commit()
    
    return None
