from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job import Job, JobStatus


class JobRepository:

    @staticmethod
    def create_job(db: Session, job: Job,) -> Job:
        db.add(job)
        db.commit()
        db.refresh(job)
        return job

    @staticmethod
    def get_by_id( db: Session, job_id: int,) -> Job | None:
        statement = select(Job).where(Job.id == job_id)
        result = db.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    def get_all_jobs(db: Session,) -> list[Job]:
        statement = select(Job)
        result = db.execute(statement)
        return result.scalars().all()

    @staticmethod
    def get_by_status(db: Session,status: JobStatus,) -> list[Job]:
        statement = select(Job).where(Job.status == status)
        result = db.execute(statement)
        return result.scalars().all()

    @staticmethod
    def get_by_creator(db: Session,created_by: int,) -> list[Job]:
        statement = select(Job).where(Job.created_by == created_by)
        result = db.execute(statement)
        return result.scalars().all()

    @staticmethod
    def update_job(db: Session,job: Job,) -> Job:
        db.commit()
        db.refresh(job)
        return job

    @staticmethod
    def delete_job(db: Session,job: Job,) -> None:
        db.delete(job)
        db.commit()