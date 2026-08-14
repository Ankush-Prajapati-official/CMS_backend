from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.application import Application, ApplicationStatus


class ApplicationRepository:

    @staticmethod
    def create_application(db: Session,application: Application,) -> Application:
        db.add(application)
        db.commit()
        db.refresh(application)
        return application

    @staticmethod
    def get_by_candidate_and_job(db: Session,candidate_id: int,job_id: int,) -> Application | None:

        statement = select(Application).where(
        Application.candidate_id == candidate_id,
        Application.job_id == job_id,
    )

        result = db.execute(statement)

        return result.scalar_one_or_none()

    @staticmethod
    def get_by_id(db: Session,application_id: int,) -> Application | None:
        statement = select(Application).where(Application.id == application_id)
        result = db.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    def get_all_applications(db: Session,) -> list[Application]:
        statement = select(Application)
        result = db.execute(statement)
        return result.scalars().all()

    @staticmethod
    def get_by_candidate(db: Session,candidate_id: int,) -> list[Application]:
        statement = select(Application).where(Application.candidate_id == candidate_id)
        result = db.execute(statement)
        return result.scalars().all()

    @staticmethod
    def get_by_job(db: Session,job_id: int,) -> list[Application]:
        statement = select(Application).where(Application.job_id == job_id)
        result = db.execute(statement)
        return result.scalars().all()

    @staticmethod
    def get_by_status(db: Session,status: ApplicationStatus,) -> list[Application]:
        statement = select(Application).where(Application.status == status)
        result = db.execute(statement)
        return result.scalars().all()

    @staticmethod
    def update_application(db: Session,application: Application,) -> Application:
        db.commit()
        db.refresh(application)
        return application

    @staticmethod
    def delete_application(db: Session,application: Application,) -> None:
        db.delete(application)
        db.commit()
