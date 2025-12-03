"""Review Pydantic Schemas - Input/Output validation for reviews"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.review import GradeEnum


class ReviewCreate(BaseModel):
    """Schema for creating a new review"""
    professor_id: int
    rating_quality: int = Field(..., ge=1, le=5, description="Quality rating 1-5")
    rating_difficulty: int = Field(..., ge=1, le=5, description="Difficulty rating 1-5")
    grade_received: GradeEnum
    comment: Optional[str] = Field(None, max_length=2000)
    course_code: Optional[str] = Field(None, max_length=20)
    semester: str = Field(..., min_length=5, max_length=20)  # e.g., "Fall 2024"
    
    class Config:
        json_schema_extra = {
            "example": {
                "professor_id": 1,
                "rating_quality": 4,
                "rating_difficulty": 3,
                "grade_received": "A",
                "comment": "Great professor, explains concepts clearly!",
                "course_code": "CS101",
                "semester": "Fall 2024"
            }
        }


class ReviewUpdate(BaseModel):
    """Schema for updating a review"""
    rating_quality: Optional[int] = Field(None, ge=1, le=5)
    rating_difficulty: Optional[int] = Field(None, ge=1, le=5)
    grade_received: Optional[GradeEnum] = None
    comment: Optional[str] = Field(None, max_length=2000)


class ReviewResponse(BaseModel):
    """Schema for review API responses"""
    id: int
    professor_id: int
    student_id: int
    rating_quality: int
    rating_difficulty: int
    grade_received: str
    comment: Optional[str]
    course_code: Optional[str]
    semester: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ReviewWithProfessor(ReviewResponse):
    """Review response that includes professor name"""
    professor_name: Optional[str] = None

