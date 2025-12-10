"""Review Flag Model - Tracks user flags on reviews"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class ReviewFlag(Base):
    """Model for tracking user flags on reviews"""
    __tablename__ = "review_flags"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    review_id = Column(Integer, ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False)
    reason = Column(String(500), nullable=True)
    flagged_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="review_flags_created")
    review = relationship("Review", back_populates="flags")
    
    # Ensure one flag per user per review
    __table_args__ = (
        UniqueConstraint('user_id', 'review_id', name='unique_user_review_flag'),
    )
    
    def __repr__(self):
        return f"<ReviewFlag(id={self.id}, user_id={self.user_id}, review_id={self.review_id})>"
