from datetime import datetime
from enum import Enum as PyEnum
from pydantic import BaseModel, ConfigDict

class ApplicationStatus(str, PyEnum):
    APPLIED = "Applied"
    SCREENING = "Screening"
    SHORTLISTED = "Shortlisted"
    INTERVIEW_SCHEDULED = "Interview Scheduled"
    INTERVIEWED = "Interviewed"
    OFFERED = "Offered"
    HIRED = "Hired"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"


class CreateApplicationSchema(BaseModel):
    candidate_id: int
    job_id: int

class UpdateApplicationSchema(BaseModel):
    status: ApplicationStatus

class ApplicationResponseSchema(BaseModel):
    id: int
    candidate_id: int
    job_id: int
    status: ApplicationStatus
    created_by: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )