"""Review Vote Model - Tracks helpful votes on reviews"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class ReviewVote(Base):
    """Model for tracking user votes on reviews"""
    __tablename__ = "review_votes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    review_id = Column(Integer, ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False)
    vote_type = Column(String(20), nullable=False, default="helpful")  # helpful or not_helpful
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="review_votes")
    review = relationship("Review", back_populates="votes")
    
    # Ensure one vote per user per review
    __table_args__ = (
        UniqueConstraint('user_id', 'review_id', name='unique_user_review_vote'),
    )
    
    def __repr__(self):
        return f"<ReviewVote(id={self.id}, user_id={self.user_id}, review_id={self.review_id}, vote_type={self.vote_type})>"
