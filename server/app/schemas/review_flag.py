from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Schema for creating a flag
class FlagCreate(BaseModel):
    review_id: int = Field(..., description="ID of the review being flagged")
    reason: Optional[str] = Field(None, max_length=500, description="Reason for flagging the review")

# Schema for flag response
class FlagResponse(BaseModel):
    id: int
    user_id: int
    review_id: int
    reason: Optional[str]
    flagged_at: datetime
    
    class Config:
        from_attributes = True
