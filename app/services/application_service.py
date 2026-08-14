from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.application import Application
from app.models.user import User
from app.repositories.application_repository import ApplicationRepository
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.job_repository import JobRepository
from app.schemas.application_schema import (CreateApplicationSchema,UpdateApplicationSchema,)


class ApplicationService:

    @staticmethod
    def create_application(db: Session,application: CreateApplicationSchema,current_user: User,):
        # Step 1: Check candidate exists
        candidate = CandidateRepository.get_by_id(
            db=db,
            candidate_id=application.candidate_id,
        )
        if candidate is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidate not found.",
            )

        # Step 2: Check job exists
        job = JobRepository.get_by_id(
            db=db,
            job_id=application.job_id,
        )
        if job is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found.",
            )

        # Step 3: Prevent duplicate application
        existing_application = (
            ApplicationRepository.get_by_candidate_and_job(
                db=db,
                candidate_id=application.candidate_id,
                job_id=application.job_id,
            )
        )

        if existing_application:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Candidate has already applied for this job.",
            )

        # Step 4: Create application
        new_application = Application(
            candidate_id=application.candidate_id,
            job_id=application.job_id,
            created_by=current_user.id,
        )

        # status defaults to APPLIED in the model
        created_application = (
            ApplicationRepository.create_application(
                db=db,
                application=new_application,
            )
        )
        # Step 5: Return response
        return {
            "success": True,
            "message": "Application created successfully.",
            "application_id": created_application.id,
        }

        # Get Application by ID
    @staticmethod
    def get_application_by_id(db: Session,application_id: int,):
        application = ApplicationRepository.get_by_id(
            db=db,
            application_id=application_id,
        )
        if application is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found.",
            )
        return application

    # Get All Applications
    @staticmethod
    def get_all_applications(db: Session,):
        return ApplicationRepository.get_all_applications(
            db=db,
        )

    # Update Application Status
    @staticmethod
    def update_application_status(db: Session,application_id: int,status_data: UpdateApplicationSchema,):
        # Step 1: Find application
        application = ApplicationRepository.get_by_id(
            db=db,
            application_id=application_id,
        )
        if application is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found.",
            )

        # Step 2: Update status
        application.status = status_data.status

        # Step 3: Save changes
        updated_application = ApplicationRepository.update_application(
            db=db,
            application=application,
        )

        # Step 4: Return response
        return {
            "success": True,
            "message": "Application status updated successfully.",
            "application_id": updated_application.id,
            "status": updated_application.status,
        }

    # Delete Application
    @staticmethod
    def delete_application(db: Session,application_id: int,):
        # Step 1: Find application
        application = ApplicationRepository.get_by_id(
            db=db,
            application_id=application_id,
        )
        if application is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found.",
            )

        # Step 2: Delete application
        ApplicationRepository.delete_application(
            db=db,
            application=application,
        )
        # Step 3: Return response
        return {
            "success": True,
            "message": "Application deleted successfully.",
        }