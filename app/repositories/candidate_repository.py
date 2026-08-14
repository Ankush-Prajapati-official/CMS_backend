from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.candidate import Candidate


class CandidateRepository:

    @staticmethod
    def create_candidate(db: Session,candidate: Candidate,) -> Candidate:
        db.add(candidate)
        db.commit()
        db.refresh(candidate)
        return candidate

    @staticmethod
    def get_by_id(db: Session,candidate_id: int,) -> Candidate | None:
        statement = select(Candidate).where(Candidate.id == candidate_id)
        result = db.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    def get_by_email(db: Session,email: str,) -> Candidate | None:
        statement = select(Candidate).where(Candidate.email == email)
        result = db.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    def get_all_candidates(db: Session,) -> list[Candidate]:
        statement = select(Candidate)
        result = db.execute(statement)
        return result.scalars().all()

    @staticmethod
    def get_by_phone(db: Session,phone: str,) -> Candidate | None:
        statement = select(Candidate).where(Candidate.phone == phone)
        result = db.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    def update_candidate(db: Session,candidate: Candidate,) -> Candidate:
        db.commit()
        db.refresh(candidate)
        return candidate

    @staticmethod
    def delete_candidate(db: Session,candidate: Candidate,) -> None:
        db.delete(candidate)
        db.commit()