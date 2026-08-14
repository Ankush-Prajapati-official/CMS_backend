from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, String, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.base_mixin import BaseMixin
from enum import Enum as PyEnum

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.application import Application


class JobStatus(str, PyEnum):
    OPEN = "Open"
    CLOSED = "Closed"
    DRAFT = "Draft"


class Job(Base, BaseMixin):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    location: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    employment_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    experience: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    salary: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    status: Mapped[JobStatus] = mapped_column(
         Enum(JobStatus),
         nullable=False,
         default=JobStatus.OPEN,
    )
    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id",ondelete = "RESTRICT"),
        nullable=False,
    )
    created_by_user: Mapped["User"] = relationship(
        back_populates="jobs",
    )
    applications: Mapped[list["Application"]] = relationship(
                back_populates="job",
               cascade="all, delete-orphan",
    )