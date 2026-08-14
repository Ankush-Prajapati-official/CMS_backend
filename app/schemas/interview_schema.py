from datetime import datetime
from enum import Enum as PyEnum
from pydantic import BaseModel, ConfigDict

class InterviewRound(str, PyEnum):
    HR = "HR"
    TECHNICAL = "Technical"
    MANAGERIAL = "Managerial"

class InterviewStatus(str, PyEnum):
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    NO_SHOW = "No Show"

class CreateInterviewSchema(BaseModel):
    application_id: int
    interviewer_id: int
    round_number: int
    round_name: InterviewRound
    scheduled_at: datetime

class UpdateInterviewSchema(BaseModel):
    interviewer_id: int | None = None
    scheduled_at: datetime | None = None
    status: InterviewStatus | None = None
    round_number: int | None = None
    round_name: str | None = None

class InterviewResponseSchema(BaseModel):
    id: int
    application_id: int
    interviewer_id: int
    created_by: int
    round_number: int
    round_name: InterviewRound
    scheduled_at: datetime
    status: InterviewStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )