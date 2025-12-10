from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

class Professor(Base):
    """Professor model - represents a professor in the system"""
    __tablename__ = "professors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    department = Column(String(100), nullable=False)
    
    # Professor claim fields
    claimed_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    is_claimed = Column(Boolean, default=False, nullable=False)
    claimed_at = Column(DateTime, nullable=True)
    is_verified = Column(Boolean, default=False)
    
    # Aggregate stats (will be calculated from reviews)
    avg_rating = Column(Float, default=0.0)
    avg_difficulty = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    
    # Relationships
    reviews = relationship("Review", backref="professor", foreign_keys="Review.professor_id")
    claimed_by = relationship("User", foreign_keys=[claimed_by_user_id])

    def __repr__(self):
        return f"<Professor(id={self.id}, name='{self.name}', dept='{self.department}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "is_verified": self.is_verified,
            "avg_rating": self.avg_rating,
            "avg_difficulty": self.avg_difficulty,
            "total_reviews": self.total_reviews
        }