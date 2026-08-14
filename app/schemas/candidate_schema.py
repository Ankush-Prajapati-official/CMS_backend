from enum import Enum as PyEnum
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class CandidateStatus(str, PyEnum):
    ACTIVE = "Active"
    HIRED = "Hired"
    ARCHIVED = "Archived"

class CreateCandidateSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    years_of_experience: float = 0.0
    current_company: str | None = None
    current_ctc: float | None = None
    expected_ctc: float | None = None
    notice_period: str | None = None
    current_location: str | None = None

class UpdateCandidateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    years_of_experience: float | None = None
    current_company: str | None = None
    current_ctc: float | None = None
    expected_ctc: float | None = None
    notice_period: str | None = None
    current_location: str | None = None
    status: CandidateStatus | None = None

class CandidateResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    years_of_experience: float
    current_company: str | None
    current_ctc: float | None
    expected_ctc: float | None
    notice_period: str | None
    current_location: str | None
    status: CandidateStatus
    created_by: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )