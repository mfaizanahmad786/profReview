# This file makes the models directory a Python package
# Import your models here so they can be easily accessed

from app.models.user import User, UserRole
from app.models.professor import Professor
from app.models.professor_follow import ProfessorFollow
from app.models.review import Review, GradeEnum
from app.models.review_vote import ReviewVote
from app.models.professor_claim_request import ProfessorClaimRequest, ClaimStatus
from app.models.review_flag import ReviewFlag

# This makes the models available when you import from app.models
__all__ = ["User", "UserRole","Professor","ProfessorFollow","Review","GradeEnum","ReviewVote","ProfessorClaimRequest","ClaimStatus","ReviewFlag"]