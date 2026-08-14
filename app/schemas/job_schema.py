from enum import Enum as PyEnum
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class JobStatus(str, PyEnum):
    OPEN = "Open"
    CLOSED = "Closed"
    DRAFT = "Draft"

class CreateJobSchema(BaseModel):
    title: str
    description: str
    location: str
    employment_type: str
    experience: str
    salary: int

class UpdateJobSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    employment_type: str | None = None
    experience: str | None = None
    salary: int | None = None
    status: JobStatus | None = None

class JobResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    location: str
    employment_type: str
    experience: str
    salary: int
    status: JobStatus
    created_by: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )