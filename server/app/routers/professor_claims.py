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
    
    # CONSTRAINT 1: Check if this professor profile is already claimed by someone
    if professor.is_claimed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This professor profile has already been claimed by another user"
        )
    
    # Also check if there's an approved claim request for this professor
    existing_claim_for_professor = db.query(ProfessorClaimRequest).filter(
        ProfessorClaimRequest.professor_id == professor_id,
        ProfessorClaimRequest.status == ClaimStatus.APPROVED
    ).first()
    
    if existing_claim_for_professor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This professor profile has already been claimed by another user"
        )
    
    # CONSTRAINT 2: Check if this user already has ANY approved claim (one claim per professor user)
    existing_approved_claim = db.query(ProfessorClaimRequest).filter(
        ProfessorClaimRequest.user_id == current_user.id,
        ProfessorClaimRequest.status == ClaimStatus.APPROVED
    ).first()
    
    if existing_approved_claim:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already claimed a professor profile. Each professor can only claim one profile."
        )
    
    # CONSTRAINT 3: Check if this user has ANY pending claim (prevent multiple simultaneous claims)
    existing_pending_claim = db.query(ProfessorClaimRequest).filter(
        ProfessorClaimRequest.user_id == current_user.id,
        ProfessorClaimRequest.status == ClaimStatus.PENDING
    ).first()
    
    if existing_pending_claim:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a pending claim request. Please wait for it to be reviewed before submitting another."
        )
    
    # Check if there's a pending claim for this specific professor by anyone
    pending_claim_for_professor = db.query(ProfessorClaimRequest).filter(
        ProfessorClaimRequest.professor_id == professor_id,
        ProfessorClaimRequest.status == ClaimStatus.PENDING
    ).first()
    
    if pending_claim_for_professor and pending_claim_for_professor.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This professor profile has a pending claim request from another user"
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
    try:
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
        
        # Convert to response if exists
        claim_response = None
        if claim_to_return:
            claim_response = ClaimRequestResponse(
                id=claim_to_return.id,
                user_id=claim_to_return.user_id,
                professor_id=claim_to_return.professor_id,
                status=claim_to_return.status.value,
                request_message=claim_to_return.request_message,
                requested_at=claim_to_return.requested_at,
                reviewed_at=claim_to_return.reviewed_at,
                reviewed_by=claim_to_return.reviewed_by,
                rejection_reason=claim_to_return.rejection_reason
            )
        
        return ClaimStatusResponse(
            has_pending=pending_claim is not None,
            has_approved=approved_claim is not None,
            has_rejected=rejected_claim is not None,
            claim_request=claim_response,
            claimed_professor_id=approved_claim.professor_id if approved_claim else None
        )
    except Exception as e:
        print(f"Error in get_my_claim_status: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting claim status: {str(e)}"
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
