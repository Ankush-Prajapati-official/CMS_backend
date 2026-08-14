from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.core.security import require_roles
from app.models.user import User
from app.schemas.feedback_schema import (CreateFeedbackSchema,UpdateFeedbackSchema,FeedbackResponseSchema,)
from app.services.feedback_service import FeedbackService


router = APIRouter(
    prefix="/api/v1/feedback",
    tags=["Feedback"],
)

# Create Feedback
@router.post("/",status_code=status.HTTP_201_CREATED,)
def create_feedback(
    feedback: CreateFeedbackSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "HR")
    ),
):
    return FeedbackService.create_feedback(
        db=db,
        feedback_data=feedback,
        current_user=current_user,
    )

# Get All Feedback
@router.get("/",response_model=list[FeedbackResponseSchema],)
def get_all_feedback(
    db: Session = Depends(get_db),
):
    return FeedbackService.get_all_feedback(
        db=db,
    )

# Get Feedback by ID
@router.get("/{feedback_id}",response_model=FeedbackResponseSchema,)
def get_feedback_by_id(
    feedback_id: int,
    db: Session = Depends(get_db),
):
    return FeedbackService.get_feedback_by_id(
        db=db,
        feedback_id=feedback_id,
    )

# Get Feedback by Interview
@router.get("/interview/{interview_id}",response_model=FeedbackResponseSchema,)
def get_feedback_by_interview(
    interview_id: int,
    db: Session = Depends(get_db),
):
    return FeedbackService.get_feedback_by_interview(
        db=db,
        interview_id=interview_id,
    )

# Update Feedback
@router.put("/{feedback_id}",)
def update_feedback(
    feedback_id: int,
    feedback: UpdateFeedbackSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "HR")
    ),
):
    return FeedbackService.update_feedback(
        db=db,
        feedback_id=feedback_id,
        feedback_data=feedback,
    )

# Delete Feedback
@router.delete("/{feedback_id}",)
def delete_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin","HR")
    ),
):
    return FeedbackService.delete_feedback(
        db=db,
        feedback_id=feedback_id,
    )