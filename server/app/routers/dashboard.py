"""Dashboard Routes - Student dashboard data"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.professor import Professor
from app.models.review import Review
from app.models.professor_follow import ProfessorFollow
from app.schemas.dashboard import DashboardResponse, DashboardStats, DashboardReviewResponse


router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/me", response_model=DashboardResponse)
def get_my_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get complete dashboard data for the current user
    - User statistics
    - Recent reviews
    - Followed professors
    """
    
    # Get user's reviews with professor info
    reviews_query = db.query(Review, Professor).join(
        Professor, Review.professor_id == Professor.id
    ).filter(
        Review.student_id == current_user.id
    ).order_by(Review.created_at.desc()).all()
    
    # Build reviews response
    recent_reviews = []
    for review, professor in reviews_query:
        recent_reviews.append(DashboardReviewResponse(
            id=review.id,
            professor_id=professor.id,
            professor_name=professor.name,
            professor_department=professor.department,
            rating_quality=review.rating_quality,
            rating_difficulty=review.rating_difficulty,
            grade_received=review.grade_received.value,
            comment=review.comment,
            course_code=review.course_code,
            semester=review.semester,
            created_at=review.created_at
        ))
    
    # Calculate statistics
    total_reviews = len(recent_reviews)
    avg_rating_given = 0.0
    if total_reviews > 0:
        avg_rating_given = sum(r.rating_quality for r in recent_reviews) / total_reviews
    
    # Get most reviewed department
    most_reviewed_dept = None
    if recent_reviews:
        dept_counts = {}
        for review in recent_reviews:
            dept = review.professor_department
            dept_counts[dept] = dept_counts.get(dept, 0) + 1
        most_reviewed_dept = max(dept_counts.items(), key=lambda x: x[1])[0]
    
    # Get followed professors count
    followed_count = db.query(ProfessorFollow).filter(
        ProfessorFollow.user_id == current_user.id
    ).count()
    
    # Get followed professors with details
    follows = db.query(ProfessorFollow, Professor).join(
        Professor, ProfessorFollow.professor_id == Professor.id
    ).filter(
        ProfessorFollow.user_id == current_user.id
    ).order_by(ProfessorFollow.followed_at.desc()).all()
    
    followed_professors = []
    for follow, professor in follows:
        followed_professors.append({
            "id": professor.id,
            "name": professor.name,
            "department": professor.department,
            "avg_rating": professor.avg_rating,
            "avg_difficulty": professor.avg_difficulty,
            "total_reviews": professor.total_reviews,
            "followed_at": follow.followed_at.isoformat()
        })
    
    # Build stats
    stats = DashboardStats(
        total_reviews=total_reviews,
        avg_rating_given=round(avg_rating_given, 2),
        total_professors_followed=followed_count,
        most_reviewed_department=most_reviewed_dept
    )
    
    return DashboardResponse(
        stats=stats,
        recent_reviews=recent_reviews,
        followed_professors=followed_professors
    )
