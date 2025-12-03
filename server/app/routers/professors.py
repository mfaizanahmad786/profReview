"""Professor Routes - CRUD operations for professors"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.models.user import User
from app.models.professor import Professor
from app.schemas.professor import ProfessorCreate, ProfessorUpdate, ProfessorResponse


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