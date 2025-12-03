import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime


from app.core.database import Base

class UserRole(str, enum.Enum):

    STUDENT = "student"
    PROFESSOR = "professor"
    ADMIN = "admin"

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.STUDENT, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role.value}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role.value,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def is_admin(self):
        return self.role == UserRole.ADMIN
    
    def is_professor(self):
        return self.role == UserRole.PROFESSOR
    
    def is_student(self):
        return self.role == UserRole.STUDENT

    
