"""User Pydantic Schemas for validation and serialization"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


class UserCreate(BaseModel):
    """Schema for user signup"""
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    role: Optional[UserRole] = Field(UserRole.STUDENT)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "student@university.edu",
                "password": "MySecurePassword123",
            }
        }


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "student@university.edu",
                "password": "MySecurePassword123"
            }
        }


class UserResponse(BaseModel):
    """Schema for API responses - NO password!"""
    id: int
    email: str
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for updating user info - all fields optional"""
    email: Optional[EmailStr] = None
    university_id: Optional[str] = Field(None, max_length=50)
    role: Optional[UserRole] = None


class Token(BaseModel):
    """JWT token response after login"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Data stored inside the JWT token"""
    email: Optional[str] = None
    role: Optional[str] = None

