from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.feedback import Feedback
from app.models.user import User
from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.interview_repository import InterviewRepository
from app.schemas.feedback_schema import (CreateFeedbackSchema,UpdateFeedbackSchema,)


class FeedbackService:

    # Create Feedback
    @staticmethod
    def create_feedback(db: Session,feedback_data: CreateFeedbackSchema,current_user: User,):
        # Step 1: Check interview exists
        interview = InterviewRepository.get_by_id(
            db=db,
            interview_id=feedback_data.interview_id,
        )
        if interview is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview not found.",
            )

        # Step 2: Check feedback already exists
        existing_feedback = FeedbackRepository.get_by_interview(
            db=db,
            interview_id=feedback_data.interview_id,
        )
        if existing_feedback:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Feedback already exists for this interview.",
            )

        # Step 3: Calculate overall rating
        overall_rating = (
            feedback_data.technical_skills_rating
            + feedback_data.communication_skills_rating
            + feedback_data.problem_solving_rating
        ) / 3

        # Step 4: Create Feedback object
        new_feedback = Feedback(
            interview_id=feedback_data.interview_id,
            technical_skills_rating=feedback_data.technical_skills_rating,
            communication_skills_rating=feedback_data.communication_skills_rating,
            problem_solving_rating=feedback_data.problem_solving_rating,
            overall_rating=overall_rating,
            recommendation=feedback_data.recommendation,
            interviewer_comments=feedback_data.comments,
        )
        # Step 5: Save Feedback
        created_feedback = FeedbackRepository.create_feedback(
            db=db,
            feedback=new_feedback,
        )
        # Step 6: Return response
        return {
            "success": True,
            "message": "Feedback created successfully.",
            "feedback_id": created_feedback.id,
        }

      # Get Feedback by ID
    @staticmethod
    def get_feedback_by_id(db: Session,feedback_id: int,):
        feedback = FeedbackRepository.get_by_id(
            db=db,
            feedback_id=feedback_id,
        )
        if feedback is None:
          raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
              detail="Feedback not found.",
             )
        return feedback

     # Get All Feedback
    @staticmethod
    def get_all_feedback(db: Session,):
       return FeedbackRepository.get_all_feedback(
          db=db,
       )

    # Get Feedback by Interview
    @staticmethod
    def get_feedback_by_interview(db: Session,interview_id: int,):
         feedback = FeedbackRepository.get_by_interview(
             db=db,
             interview_id=interview_id,
        )     
         if feedback is None:
            raise HTTPException(
                 status_code=status.HTTP_404_NOT_FOUND,
                 detail="Feedback not found for this interview.",
                )

         return feedback


     # Update Feedback
    @staticmethod
    def update_feedback(db: Session,feedback_id: int,feedback_data: UpdateFeedbackSchema,):
        # Step 1: Find feedback
          feedback = FeedbackRepository.get_by_id(
             db=db,
             feedback_id=feedback_id,
          )
          if feedback is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feedback not found.",
            )

      # Step 2: Update provided fields
          if feedback_data.technical_skills_rating is not None:
            feedback.technical_skills_rating = (feedback_data.technical_skills_rating)

          if feedback_data.communication_skills_rating is not None:
              feedback.communication_skills_rating = (feedback_data.communication_skills_rating)

          if feedback_data.problem_solving_rating is not None:
              feedback.problem_solving_rating = (feedback_data.problem_solving_rating)

          if feedback_data.recommendation is not None:
            feedback.recommendation = feedback_data.recommendation

          if feedback_data.comments is not None:
            feedback.comments = feedback_data.comments

     # Step 3: calculate overall rating
          feedback.overall_rating = (
            feedback.technical_skills_rating
          + feedback.communication_skills_rating
          + feedback.problem_solving_rating
        ) / 3

       # Step 4: Save
          updated_feedback = FeedbackRepository.update_feedback(
              db=db,
            feedback=feedback,
          )
          return {
               "success": True,
                "message": "Feedback updated successfully.",
                 "feedback_id": updated_feedback.id,
            }


    # Delete Feedback
    @staticmethod
    def delete_feedback(db: Session,feedback_id: int,):
    # Step 1: Find feedback
       feedback = FeedbackRepository.get_by_id(
             db=db,
            feedback_id=feedback_id,
         )
       if feedback is None:
             raise HTTPException(
                 status_code=status.HTTP_404_NOT_FOUND,
                 detail="Feedback not found.",
            )

     # Step 2: Delete
       FeedbackRepository.delete_feedback(
            db=db,
            feedback=feedback,
        )
       return {
            "success": True,
            "message": "Feedback deleted successfully.",
        }