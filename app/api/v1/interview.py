from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.core.security import require_roles
from app.models.user import User
from app.schemas.interview_schema import (CreateInterviewSchema,UpdateInterviewSchema,InterviewResponseSchema,)
from app.services.interview_service import InterviewService

router = APIRouter(
    prefix="/api/v1/interviews",
    tags=["Interviews"],
)


# Create / Schedule Interview
@router.post("/",status_code=status.HTTP_201_CREATED,)
def create_interview(
    interview: CreateInterviewSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "HR")
    ),
):
    return InterviewService.create_interview(
        db=db,
        interview_data=interview,
        current_user=current_user,
    )

# Get All Interviews
@router.get("/",response_model=list[InterviewResponseSchema],)
def get_all_interviews(db: Session = Depends(get_db),):
    return InterviewService.get_all_interviews(
        db=db,
    )

# Get Interview by ID
@router.get("/{interview_id}",response_model=InterviewResponseSchema)
def get_interview_by_id(
    interview_id: int,
    db: Session = Depends(get_db),
):
    return InterviewService.get_interview_by_id(
        db=db,
        interview_id=interview_id,
    )

# Update Interview
@router.put("/{interview_id}",)
def update_interview(
    interview_id: int,
    interview: UpdateInterviewSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "HR")
    ),
):
    return InterviewService.update_interview(
        db=db,
        interview_id=interview_id,
        interview_data=interview,
    )

# Delete Interview
@router.delete("/{interview_id}",)
def delete_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "HR")
    ),
):
    return InterviewService.delete_interview(
        db=db,
        interview_id=interview_id,
    )