from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.base_mixin import BaseMixin

if TYPE_CHECKING:
    from app.models.user import User
    



class Role(Base, BaseMixin):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
     )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
     )
    users: Mapped[list["User"]] = relationship(
        back_populates="role"
     )