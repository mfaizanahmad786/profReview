"""Professor Routes - CRUD operations for professors"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.models.user import User, UserRole
from app.models.professor import Professor
from app.models.professor_follow import ProfessorFollow
from app.schemas.professor import (
    ProfessorCreate, 
    ProfessorUpdate, 
    ProfessorResponse,
    ProfessorFollowResponse,
    FollowedProfessorResponse
)


router = APIRouter(prefix="/professors", tags=["Professors"])


@router.get("", response_model=List[ProfessorResponse])
def list_professors(
    search: str = Query(None, description="Search by name"),
    department: str = Query(None, description="Filter by department"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List all professors with optional search and filtering"""
    query = db.query(Professor)
    
    if search:
        query = query.filter(Professor.name.ilike(f"%{search}%"))
    
    if department:
        query = query.filter(Professor.department.ilike(f"%{department}%"))
    
    professors = query.offset(skip).limit(limit).all()
    return professors


@router.get("/{professor_id}", response_model=ProfessorResponse)
def get_professor(professor_id: int, db: Session = Depends(get_db)):
    """Get a specific professor by ID"""
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    
    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor not found"
        )
    
    return professor


@router.post("", response_model=ProfessorResponse, status_code=status.HTTP_201_CREATED)
def create_professor(
    professor_data: ProfessorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Create a new professor (admin only)"""
    new_professor = Professor(
        name=professor_data.name,
        department=professor_data.department
    )
    
    db.add(new_professor)
    db.commit()
    db.refresh(new_professor)
    
    return new_professor


@router.put("/{professor_id}", response_model=ProfessorResponse)
def update_professor(
    professor_id: int,
    professor_data: ProfessorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Update a professor (admin only)"""
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    
    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor not found"
        )
    
    # Update only provided fields
    if professor_data.name is not None:
        professor.name = professor_data.name
    if professor_data.department is not None:
        professor.department = professor_data.department
    
    db.commit()
    db.refresh(professor)
    
    return professor


@router.post("/{professor_id}/follow", response_model=ProfessorFollowResponse)
def follow_professor(
    professor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Follow a professor - Only students can follow professors"""
    # Block professors from following other professors
    if current_user.role == UserRole.PROFESSOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Professors cannot follow other professors. Only students can follow professors."
        )
    
    # Check if professor exists
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor not found"
        )
    
    # Check if already following
    existing_follow = db.query(ProfessorFollow).filter(
        and_(
            ProfessorFollow.user_id == current_user.id,
            ProfessorFollow.professor_id == professor_id
        )
    ).first()
    
    if existing_follow:
        return ProfessorFollowResponse(
            professor_id=professor_id,
            is_following=True,
            message="Already following this professor"
        )
    
    # Create follow
    new_follow = ProfessorFollow(
        user_id=current_user.id,
        professor_id=professor_id
    )
    
    db.add(new_follow)
    db.commit()
    
    return ProfessorFollowResponse(
        professor_id=professor_id,
        is_following=True,
        message="Successfully followed professor"
    )


@router.delete("/{professor_id}/unfollow", response_model=ProfessorFollowResponse)
def unfollow_professor(
    professor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Unfollow a professor"""
    # Check if professor exists
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor not found"
        )
    
    # Find and delete follow
    follow = db.query(ProfessorFollow).filter(
        and_(
            ProfessorFollow.user_id == current_user.id,
            ProfessorFollow.professor_id == professor_id
        )
    ).first()
    
    if not follow:
        return ProfessorFollowResponse(
            professor_id=professor_id,
            is_following=False,
            message="Not following this professor"
        )
    
    db.delete(follow)
    db.commit()
    
    return ProfessorFollowResponse(
        professor_id=professor_id,
        is_following=False,
        message="Successfully unfollowed professor"
    )


@router.get("/{professor_id}/is-following")
def check_is_following(
    professor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Check if current user is following a professor"""
    follow = db.query(ProfessorFollow).filter(
        and_(
            ProfessorFollow.user_id == current_user.id,
            ProfessorFollow.professor_id == professor_id
        )
    ).first()
    
    return {"is_following": follow is not None}


@router.get("/following/list", response_model=List[FollowedProfessorResponse])
def get_followed_professors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all professors followed by the current user"""
    follows = db.query(ProfessorFollow, Professor).join(
        Professor, ProfessorFollow.professor_id == Professor.id
    ).filter(
        ProfessorFollow.user_id == current_user.id
    ).order_by(ProfessorFollow.followed_at.desc()).all()
    
    result = []
    for follow, professor in follows:
        result.append(FollowedProfessorResponse(
            id=professor.id,
            name=professor.name,
            department=professor.department,
            avg_rating=professor.avg_rating,
            avg_difficulty=professor.avg_difficulty,
            total_reviews=professor.total_reviews,
            followed_at=follow.followed_at
        ))
    
    return result