from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.interview import Interview
from app.models.user import User
from app.repositories.interview_repository import InterviewRepository
from app.repositories.application_repository import ApplicationRepository
from app.repositories.user_repository import UserRepository
from app.schemas.interview_schema import (CreateInterviewSchema,UpdateInterviewSchema,)


class InterviewService:

    # Create / Schedule Interview
    @staticmethod
    def create_interview(
        db: Session,
        interview_data: CreateInterviewSchema,
        current_user: User,
    ):

        # Step 1: Check application exists
        application = ApplicationRepository.get_by_id(
            db=db,
            application_id=interview_data.application_id,
        )

        if application is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found.",
            )

        # Step 2: Check interviewer exists
        interviewer = UserRepository.get_by_id(
            db=db,
            user_id=interview_data.interviewer_id,
        )

        if interviewer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interviewer not found.",
            )

        # Step 3: Check duplicate interview round
        existing_interview = (
            InterviewRepository.get_by_application_and_round(
                db=db,
                application_id=interview_data.application_id,
                round_number=interview_data.round_number,
            )
        )

        if existing_interview:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This interview round already exists for this application.",
            )

        # Step 4: Create Interview object
        new_interview = Interview(
            application_id=interview_data.application_id,
            interviewer_id=interview_data.interviewer_id,
            created_by=current_user.id,
            round_number=interview_data.round_number,
            round_name=interview_data.round_name,
            scheduled_at=interview_data.scheduled_at,
        )

        # status defaults to SCHEDULED

        # Step 5: Save interview
        created_interview = InterviewRepository.create_interview(
            db=db,
            interview=new_interview,
        )

        # Step 6: Return response
        return {
            "success": True,
            "message": "Interview scheduled successfully.",
            "interview_id": created_interview.id,
        }

        # Get Interview by ID
    @staticmethod
    def get_interview_by_id(db: Session,interview_id: int,):
        interview = InterviewRepository.get_by_id(
            db=db,
            interview_id=interview_id,
        )
        if interview is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview not found.",
            )
        return interview

    # Get All Interviews
    @staticmethod
    def get_all_interviews(db: Session,):
        return InterviewRepository.get_all_interviews(
            db=db,
        )
    # Update Interview
    @staticmethod
    def update_interview(db: Session,interview_id: int,interview_data: UpdateInterviewSchema,):
        # Step 1: Find interview
        interview = InterviewRepository.get_by_id(
            db=db,
            interview_id=interview_id,
        )
        if interview is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview not found.",
            )

        # Step 2: Update provided fields

        if interview_data.interviewer_id is not None:
            interview.interviewer_id = interview_data.interviewer_id

        if interview_data.round_number is not None:
            interview.round_number = interview_data.round_number

        if interview_data.round_name is not None:
            interview.round_name = interview_data.round_name

        if interview_data.scheduled_at is not None:
            interview.scheduled_at = interview_data.scheduled_at

        if interview_data.status is not None:
            interview.status = interview_data.status

        # Step 3: Save changes
        updated_interview = InterviewRepository.update_interview(
            db=db,
            interview=interview,
        )

        # Step 4: Return response
        return {
            "success": True,
            "message": "Interview updated successfully.",
            "interview_id": updated_interview.id,
        }

    # Delete Interview
    @staticmethod
    def delete_interview(
        db: Session,
        interview_id: int,
    ):
        # Step 1: Find interview
        interview = InterviewRepository.get_by_id(
            db=db,
            interview_id=interview_id,
        )

        if interview is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview not found.",
            )

        # Step 2: Delete interview
        InterviewRepository.delete_interview(
            db=db,
            interview=interview,
        )

        # Step 3: Return response
        return {
            "success": True,
            "message": "Interview deleted successfully.",
        }

    