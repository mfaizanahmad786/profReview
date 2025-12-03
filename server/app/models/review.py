"""Review Database Model - The heart of grade distribution data"""

import enum
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class GradeEnum(str, enum.Enum):
    """Possible grades a student can receive"""
    A = "A"
    A_MINUS = "A-"
    B_PLUS = "B+"
    B = "B"
    B_MINUS = "B-"
    C_PLUS = "C+"
    C = "C"
    C_MINUS = "C-"
    D = "D"
    F = "F"
    W = "W"  # Withdrawn


class Review(Base):
    """Review model - stores student reviews with grade data"""
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign keys - links to professor and student
    professor_id = Column(Integer, ForeignKey("professors.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Ratings (1-5 scale)
    rating_quality = Column(Integer, nullable=False)  # How good is the teaching?
    rating_difficulty = Column(Integer, nullable=False)  # How hard is the course?
    
    # THE KEY FIELD - This feeds the grade distribution chart!
    grade_received = Column(SQLEnum(GradeEnum), nullable=False)
    
    # Review content
    comment = Column(Text, nullable=True)
    course_code = Column(String(20), nullable=True)  # e.g., "CS101"
    semester = Column(String(20), nullable=False)  # e.g., "Fall 2024"
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_hidden = Column(Integer, default=0)  # For admin moderation
    
    # Prevent duplicate reviews: 1 review per professor per semester
    __table_args__ = (
        UniqueConstraint('professor_id', 'student_id', 'semester', name='unique_review_per_semester'),
    )

    def __repr__(self):
        return f"<Review(id={self.id}, professor_id={self.professor_id}, grade='{self.grade_received.value}')>"