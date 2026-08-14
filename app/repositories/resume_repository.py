from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.resume import Resume


class ResumeRepository:

    @staticmethod
    def create_resume(db: Session,resume: Resume,) -> Resume:
        db.add(resume)
        db.commit()
        db.refresh(resume)
        return resume

    @staticmethod
    def get_by_id(db: Session,resume_id: int,) -> Resume | None:
        statement = select(Resume).where(Resume.id == resume_id)
        result = db.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    def get_by_candidate_id(db: Session,candidate_id: int,) -> Resume | None:
        statement = select(Resume).where(Resume.candidate_id == candidate_id)
        result = db.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    def update_resume(db: Session,resume: Resume,) -> Resume:
        db.commit()
        db.refresh(resume)
        return resume

    @staticmethod
    def delete_resume(db: Session,resume: Resume,) -> None:
        db.delete(resume)
        db.commit()