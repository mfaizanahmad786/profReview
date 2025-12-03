from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

class Professor(Base):
    """Professor model - represents a professor in the system"""
    __tablename__ = "professors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    department = Column(String(100), nullable=False)
    
    # Optional: Professor can claim their profile
    claimed_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_verified = Column(Boolean, default=False)
    
    # Aggregate stats (will be calculated from reviews)
    avg_rating = Column(Float, default=0.0)
    avg_difficulty = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    
    # Relationships
    # reviews = relationship("Review", back_populates="professor")  # Uncomment in Phase 3

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