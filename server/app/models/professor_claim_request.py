"""Professor Claim Request Model - Manages professor profile claiming"""

import enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.core.database import Base


class ClaimStatus(str, enum.Enum):
    """Status of a professor claim request"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ProfessorClaimRequest(Base):
    """Model for professor profile claim requests"""
    __tablename__ = "professor_claim_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    professor_id = Column(Integer, ForeignKey("professors.id", ondelete="CASCADE"), nullable=False)
    status = Column(SQLEnum(ClaimStatus), default=ClaimStatus.PENDING, nullable=False)
    request_message = Column(Text, nullable=True)
    requested_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    reviewed_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], backref="claim_requests")
    professor = relationship("Professor", backref="claim_requests")
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    
    # Ensure one user can only claim one professor profile (prevent duplicate requests)
    __table_args__ = (
        UniqueConstraint('user_id', 'professor_id', name='unique_user_professor_claim'),
    )
    
    def __repr__(self):
        return f"<ProfessorClaimRequest(id={self.id}, user_id={self.user_id}, professor_id={self.professor_id}, status={self.status.value})>"
    
    def approve(self, admin_user_id: int):
        """Approve the claim request"""
        self.status = ClaimStatus.APPROVED
        self.reviewed_at = datetime.utcnow()
        self.reviewed_by = admin_user_id
    
    def reject(self, admin_user_id: int, reason: str = None):
        """Reject the claim request"""
        self.status = ClaimStatus.REJECTED
        self.reviewed_at = datetime.utcnow()
        self.reviewed_by = admin_user_id
        self.rejection_reason = reason
