from __future__ import annotations
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.base_mixin import BaseMixin
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.user import User


class RefreshToken(Base, BaseMixin):
    __tablename__ = "refresh_tokens"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token: Mapped[str] = mapped_column(
        String(500),
        unique=True,
        nullable=False,
        index=True,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    user: Mapped["User"] = relationship(
        back_populates="refresh_tokens",
    )