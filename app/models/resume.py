from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.base_mixin import BaseMixin

if TYPE_CHECKING:
    from app.models.candidate import Candidate


class Resume(Base, BaseMixin):
    __tablename__ = "resumes"

    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    stored_file_name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    candidate: Mapped["Candidate"] = relationship(
        back_populates="resume",
    )
