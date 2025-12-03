from app.schemas.user import (
    UserCreate, UserLogin, UserResponse, UserUpdate, Token, TokenData
)
from app.schemas.professor import (
    ProfessorCreate, ProfessorUpdate, ProfessorResponse
)
from app.schemas.review import (
    ReviewCreate, ReviewUpdate, ReviewResponse
)

__all__ = [
    "UserCreate", "UserLogin", "UserResponse", "UserUpdate", "Token", "TokenData",
    "ProfessorCreate", "ProfessorUpdate", "ProfessorResponse",
    "ReviewCreate", "ReviewUpdate", "ReviewResponse"
]