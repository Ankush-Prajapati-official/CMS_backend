from __future__ import annotations

from enum import Enum as PyEnum
from typing import TYPE_CHECKING

from sqlalchemy import Enum, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.base_mixin import BaseMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.resume import Resume
    from app.models.application import Application


class CandidateStatus(str, PyEnum):
    ACTIVE = "Active"
    HIRED = "Hired"
    ARCHIVED = "Archived"

class Candidate(Base, BaseMixin):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        String(15),
        unique=True,
        nullable=False,
    )

    years_of_experience: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    current_company: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    current_ctc: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    expected_ctc: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    notice_period: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    current_location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    status: Mapped[CandidateStatus] = mapped_column(
        Enum(CandidateStatus),
        default=CandidateStatus.ACTIVE,
        nullable=False,
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    created_by_user: Mapped["User"] = relationship(
        back_populates="candidates",
    )

    resume: Mapped["Resume"] = relationship(
        back_populates="candidate",
        uselist=False,
        cascade="all, delete-orphan",
    )

    applications: Mapped[list["Application"]] = relationship(
        back_populates="candidate",
        cascade="all, delete-orphan",  #If the parent (Candidate) is deleted, automatically delete the related child objects (Resume, Application)."
    )
       