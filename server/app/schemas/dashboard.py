"""Dashboard Pydantic Schemas"""

from pydantic import BaseModel
from typing import List
from datetime import datetime


class DashboardReviewResponse(BaseModel):
    """Review with professor info for dashboard"""
    id: int
    professor_id: int
    professor_name: str
    professor_department: str
    rating_quality: int
    rating_difficulty: int
    grade_received: str
    comment: str | None
    course_code: str | None
    semester: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    """User statistics for dashboard"""
    total_reviews: int
    avg_rating_given: float
    total_professors_followed: int
    most_reviewed_department: str | None


class DashboardResponse(BaseModel):
    """Complete dashboard data"""
    stats: DashboardStats
    recent_reviews: List[DashboardReviewResponse]
    followed_professors: List[dict]
