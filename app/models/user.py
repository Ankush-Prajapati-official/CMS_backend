from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.base_mixin import BaseMixin
from datetime import datetime
from sqlalchemy import DateTime
if TYPE_CHECKING:
    from app.models.role import Role
    from app.models.job import Job
    from app.models.candidate import Candidate
    from app.models.application import Application
    from app.models.interview import Interview
    from app.models.refresh_token import RefreshToken


class User(Base, BaseMixin):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
     )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
      )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
      )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
      )

    reset_password_token: Mapped[str | None] = mapped_column(
         String(255),
         nullable=True,
   )
    
    reset_password_token_expires: Mapped[datetime | None] = mapped_column(
          DateTime(timezone=True),
          nullable=True,
    )    

    phone: Mapped[str | None] = mapped_column(
        String(15),
        nullable=True
      )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
      )

    #  database relationship (foreign)
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="RESTRICT"),
        nullable=False
      )

    # Object-to-object relationship handled by SQLAlchemy
    # Allows us to access user.role directly.
    role: Mapped["Role"] = relationship(#why Role is double quotted because to avoid circular import, after loading every model, later resolve this Role class
        back_populates="users"
      )
    
    jobs: Mapped[list["Job"]] = relationship(
         back_populates="created_by_user",
    )

    candidates: Mapped[list["Candidate"]] = relationship(
         back_populates="created_by_user",
    )
    applications: Mapped[list["Application"]] = relationship(
         back_populates="created_by_user",
    )

    assigned_interviews: Mapped[list["Interview"]] = relationship(
            foreign_keys="Interview.interviewer_id",
           back_populates="interviewer",
    )

    scheduled_interviews: Mapped[list["Interview"]] = relationship(
         foreign_keys="Interview.created_by",
         back_populates="created_by_user",
    )
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
    back_populates="user",
    cascade="all, delete-orphan",
)


   