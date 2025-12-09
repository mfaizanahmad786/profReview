"""Professor Follow Model - for students following professors"""

from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from datetime import datetime

from app.core.database import Base


class ProfessorFollow(Base):
    """Model for tracking which students follow which professors"""
    __tablename__ = "professor_follows"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    professor_id = Column(Integer, ForeignKey("professors.id", ondelete="CASCADE"), nullable=False, index=True)
    followed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Ensure a user can only follow a professor once
    __table_args__ = (
        UniqueConstraint('user_id', 'professor_id', name='unique_user_professor_follow'),
    )

    def __repr__(self):
        return f"<ProfessorFollow(user_id={self.user_id}, professor_id={self.professor_id})>"
