from datetime import datetime
from enum import Enum as PyEnum
from pydantic import BaseModel, ConfigDict, Field

class Recommendation(str, PyEnum):
    HIRE = "Hire"
    HOLD = "Hold"
    REJECT = "Reject"

class CreateFeedbackSchema(BaseModel):
    interview_id:int
    technical_skills_rating: int = Field(..., ge=1, le=5)
    communication_skills_rating: int = Field(..., ge=1, le=5)
    problem_solving_rating: int = Field(..., ge=1, le=5)
    recommendation: Recommendation
    comments: str | None = None

class UpdateFeedbackSchema(BaseModel):
    technical_skills_rating: int | None = Field(None, ge=1, le=5)
    communication_skills_rating: int | None = Field(None, ge=1, le=5)
    problem_solving_rating: int | None = Field(None, ge=1, le=5)
    recommendation: Recommendation | None = None
    comments: str | None = None

class FeedbackResponseSchema(BaseModel):
    id: int
    interview_id: int
    technical_skills_rating: int
    communication_skills_rating: int
    problem_solving_rating: int
    overall_rating: float
    recommendation: Recommendation
    comments: str | None = Field(
        default=None,
        validation_alias="interviewer_comments"
    )
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )