"""Professor Claim Request Pydantic Schemas"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.professor_claim_request import ClaimStatus


class ClaimRequestCreate(BaseModel):
    """Schema for creating a claim request"""
    professor_id: int
    request_message: Optional[str] = Field(None, max_length=1000, description="Why are you claiming this profile?")
    
    class Config:
        json_schema_extra = {
            "example": {
                "professor_id": 1,
                "request_message": "I am Dr. John Smith, teaching Computer Science at this university since 2015."
            }
        }


class ClaimRequestResponse(BaseModel):
    """Schema for claim request responses"""
    id: int
    user_id: int
    professor_id: int
    status: str
    request_message: Optional[str]
    requested_at: datetime
    reviewed_at: Optional[datetime]
    reviewed_by: Optional[int]
    rejection_reason: Optional[str]
    
    class Config:
        from_attributes = True


class ClaimRequestWithDetails(ClaimRequestResponse):
    """Claim request with professor and user details (for admin)"""
    professor_name: Optional[str] = None
    professor_department: Optional[str] = None
    user_email: Optional[str] = None


class ClaimStatusResponse(BaseModel):
    """Simple status check response"""
    has_pending: bool
    has_approved: bool
    has_rejected: bool
    claim_request: Optional[ClaimRequestResponse] = None
    claimed_professor_id: Optional[int] = None


class ClaimApprovalRequest(BaseModel):
    """Schema for admin approving a claim"""
    pass


class ClaimRejectionRequest(BaseModel):
    """Schema for admin rejecting a claim"""
    rejection_reason: str = Field(..., min_length=10, max_length=500, description="Reason for rejection")
