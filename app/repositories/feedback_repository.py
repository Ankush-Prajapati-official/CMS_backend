from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.feedback import Feedback


class FeedbackRepository:

    @staticmethod
    def create_feedback(db: Session,feedback: Feedback,) -> Feedback:
        db.add(feedback)
        db.commit()
        db.refresh(feedback)
        return feedback

    @staticmethod
    def get_by_id(db: Session,feedback_id: int,) -> Feedback | None:
        statement = select(Feedback).where(Feedback.id == feedback_id)
        result = db.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    def get_by_interview(db: Session,interview_id: int,) -> Feedback | None:
        statement = select(Feedback).where(Feedback.interview_id == interview_id)
        result = db.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    def get_all_feedback(db: Session,) -> list[Feedback]:
        statement = select(Feedback)
        result = db.execute(statement)
        return result.scalars().all()

    @staticmethod
    def update_feedback(db: Session,feedback: Feedback,) -> Feedback:
        db.commit()
        db.refresh(feedback)
        return feedback

    @staticmethod
    def delete_feedback(db: Session,feedback: Feedback,) -> None:
        db.delete(feedback)
        db.commit()