from __future__ import annotations
from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String,UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.base_mixin import BaseMixin

if TYPE_CHECKING:
    from app.models.application import Application
    from app.models.user import User
    from app.models.feedback import Feedback


class InterviewRound(str, PyEnum):
    HR = "HR"
    TECHNICAL = "Technical"
    MANAGERIAL = "Managerial"

class InterviewStatus(str, PyEnum):
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    NO_SHOW = "No Show"


class Interview(Base, BaseMixin):
    __tablename__ = "interviews"

    __table_args__ = (
        UniqueConstraint(
            "application_id",
            "round_number",
            name="uq_application_round",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False,
    )

    interviewer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id",ondelete="RESTRICT"),
        nullable=False,
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    round_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    round_name: Mapped[InterviewRound] = mapped_column(
        Enum(InterviewRound),
        nullable=False,
    )

    scheduled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    status: Mapped[InterviewStatus] = mapped_column(
        Enum(InterviewStatus),
        nullable=False,
        default=InterviewStatus.SCHEDULED,
    )

    application: Mapped["Application"] = relationship(
        back_populates="interviews",
    )

    interviewer: Mapped["User"] = relationship(
        foreign_keys=[interviewer_id],
        back_populates="assigned_interviews",
    )

    created_by_user: Mapped["User"] = relationship(
        foreign_keys=[created_by],
        back_populates="scheduled_interviews",
    )

    feedback: Mapped["Feedback"] = relationship(
        back_populates="interview",
        uselist=False,
        cascade="all, delete-orphan",
    )


