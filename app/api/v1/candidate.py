from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.core.security import require_roles
from app.models.user import User
from app.schemas.candidate_schema import (CreateCandidateSchema,UpdateCandidateSchema,CandidateResponseSchema,)
from app.services.candidate_service import CandidateService


router = APIRouter(
    prefix="/api/v1/candidates",
    tags=["Candidates"],
)

# Create Candidate API
@router.post("/",status_code=status.HTTP_201_CREATED,)
def create_candidate(
    candidate: CreateCandidateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "HR")
    ),
):
    return CandidateService.create_candidate(
        db=db,
        candidate=candidate,
        current_user=current_user,
    )

# Get All Candidates
@router.get("/",response_model=list[CandidateResponseSchema],)
def get_all_candidates(db: Session = Depends(get_db),):
    return CandidateService.get_all_candidates(
        db=db,
    )

# Get Candidate by ID
@router.get("/{candidate_id}",response_model=CandidateResponseSchema,)
def get_candidate_by_id(
    candidate_id: int,
    db: Session = Depends(get_db),
):
    return CandidateService.get_candidate_by_id(
        db=db,
        candidate_id=candidate_id,
    )

# Update Candidate
@router.put("/{candidate_id}",)
def update_candidate(
    candidate_id: int,
    candidate: UpdateCandidateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "HR")
    ),
):
    return CandidateService.update_candidate(
        db=db,
        candidate_id=candidate_id,
        candidate_data=candidate,
    )

# Delete Candidate
@router.delete("/{candidate_id}",)
def delete_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "HR")
    ),
):
    return CandidateService.delete_candidate(
        db=db,
        candidate_id=candidate_id,
    )