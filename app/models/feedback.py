from __future__ import annotations
from enum import Enum as PyEnum
from typing import TYPE_CHECKING
from sqlalchemy import (CheckConstraint,Enum,Float,ForeignKey,Integer,Text,)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.base_mixin import BaseMixin

if TYPE_CHECKING:
    from app.models.interview import Interview


class Recommendation(str, PyEnum):
    HIRE = "Hire"
    HOLD = "Hold"
    REJECT = "Reject"


class Feedback(Base, BaseMixin):
    __tablename__ = "feedback"

    __table_args__ = (
        CheckConstraint(
            "technical_skills_rating BETWEEN 1 AND 5",
            name="ck_technical_skills_rating",
        ),
        CheckConstraint(
            "communication_skills_rating BETWEEN 1 AND 5",
            name="ck_communication_skills_rating",
        ),
        CheckConstraint(
            "problem_solving_rating BETWEEN 1 AND 5",
            name="ck_problem_solving_rating",
        ),
        CheckConstraint(
            "overall_rating BETWEEN 1 AND 5",
            name="ck_overall_rating",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    interview_id: Mapped[int] = mapped_column(
        ForeignKey("interviews.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    technical_skills_rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    communication_skills_rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    problem_solving_rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    overall_rating: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    recommendation: Mapped[Recommendation] = mapped_column(
        Enum(Recommendation),
        nullable=False,
    )

    interviewer_comments: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    interview: Mapped["Interview"] = relationship(
        back_populates="feedback",
    )