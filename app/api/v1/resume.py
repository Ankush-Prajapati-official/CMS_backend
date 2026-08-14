from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.core.security import require_roles
from app.models.user import User
from app.services.resume_service import ResumeService


router = APIRouter(
    prefix="/api/v1/resume",
    tags=["Resume"],
)

@router.post("/upload")
def upload_resume(
    candidate_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "HR")
    ),
):
    return ResumeService.upload_resume(
        db=db,
        candidate_id=candidate_id,
        file=file,
    )

@router.delete("/{candidate_id}")
def delete_resume(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "HR")
    ),
):
    return ResumeService.delete_resume(
        db=db,
        candidate_id=candidate_id,
    )