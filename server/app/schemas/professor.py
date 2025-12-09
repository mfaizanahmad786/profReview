"""Professor Pydantic Schemas"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProfessorCreate(BaseModel):
    """Schema for creating a professor"""
    name: str = Field(..., min_length=2, max_length=255)
    department: str = Field(..., min_length=2, max_length=100)


class ProfessorUpdate(BaseModel):
    """Schema for updating a professor"""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    department: Optional[str] = Field(None, min_length=2, max_length=100)


class ProfessorResponse(BaseModel):
    """Schema for professor API responses"""
    id: int
    name: str
    department: str
    is_verified: bool
    avg_rating: float
    avg_difficulty: float
    total_reviews: int
    
    class Config:
        from_attributes = True


class ProfessorFollowResponse(BaseModel):
    """Schema for follow/unfollow response"""
    professor_id: int
    is_following: bool
    message: str


class FollowedProfessorResponse(BaseModel):
    """Schema for followed professor with follow info"""
    id: int
    name: str
    department: str
    avg_rating: float
    avg_difficulty: float
    total_reviews: int
    followed_at: datetime
    
    class Config:
        from_attributes = True