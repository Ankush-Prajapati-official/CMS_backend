from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.interview import Interview, InterviewStatus


class InterviewRepository:

    @staticmethod
    def create_interview(db: Session,interview: Interview,) -> Interview:
        db.add(interview)
        db.commit()
        db.refresh(interview)
        return interview

    @staticmethod
    def get_by_id(db: Session,interview_id: int,) -> Interview | None:
        statement = select(Interview).where(Interview.id == interview_id)
        result = db.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    def get_all_interviews(db: Session,) -> list[Interview]:
        statement = select(Interview)
        result = db.execute(statement)
        return result.scalars().all()

    @staticmethod
    def get_by_application(db: Session,application_id: int,) -> list[Interview]:
        statement = select(Interview).where(Interview.application_id == application_id)
        result = db.execute(statement)
        return result.scalars().all()

    @staticmethod
    def get_by_application_and_round(db: Session,application_id: int,round_number: int,) -> Interview | None:
        statement = select(Interview).where(Interview.application_id == application_id,Interview.round_number == round_number,)
        result = db.execute(statement)
        return result.scalar_one_or_none()
    
    @staticmethod
    def get_by_interviewer(db: Session,interviewer_id: int,) -> list[Interview]:
        statement = select(Interview).where(Interview.interviewer_id == interviewer_id)
        result = db.execute(statement)
        return result.scalars().all()

    @staticmethod
    def get_by_status(db: Session,status: InterviewStatus,) -> list[Interview]:
        statement = select(Interview).where(Interview.status == status)
        result = db.execute(statement)
        return result.scalars().all()

    @staticmethod
    def update_interview(db: Session,interview: Interview,) -> Interview:
        db.commit()
        db.refresh(interview)
        return interview

    @staticmethod
    def delete_interview(db: Session,interview: Interview,) -> None:
        db.delete(interview)
        db.commit()