from __future__ import annotations

from enum import Enum as PyEnum
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.base_mixin import BaseMixin

if TYPE_CHECKING:
    from app.models.candidate import Candidate
    from app.models.job import Job
    from app.models.user import User
    from app.models.interview import Interview


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


class Application(Base, BaseMixin):
    __tablename__ = "applications"

    #  candidate can have only one application for the same job
    __table_args__ = (
        UniqueConstraint(
            "candidate_id",
            "job_id",
            name="uq_candidate_job",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus),
        nullable=False,
        default=ApplicationStatus.APPLIED,
    )

    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False,
    )

    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    candidate: Mapped["Candidate"] = relationship(
        back_populates="applications",
    )

    job: Mapped["Job"] = relationship(
        back_populates="applications",
    )

    created_by_user: Mapped["User"] = relationship(
        back_populates="applications",
    )

    interviews: Mapped[list["Interview"]] = relationship(
        back_populates="application",
        cascade="all, delete-orphan",
    )