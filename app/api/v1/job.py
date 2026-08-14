from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.core.security import (require_roles,)
from app.models.user import User
from app.schemas.job_schema import (CreateJobSchema,UpdateJobSchema,JobResponseSchema,)
from app.services.job_service import JobService
from fastapi import HTTPException,status

router = APIRouter(
    prefix="/api/v1/jobs",
    tags=["Jobs"],
)

# create job API 
@router.post("/", status_code=status.HTTP_200_OK)
def create_job(
    job: CreateJobSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "HR")
    ),
):
    return JobService.create_job(
        db=db,
        job=job,
        current_user=current_user,
    )


# get all the job data 
@router.get("/",response_model=list[JobResponseSchema],)
def get_all_jobs(
    db: Session = Depends(get_db),
):
    return JobService.get_all_jobs(
        db=db,
    )


# get job data by job_id 
@router.get("/{job_id}",response_model=JobResponseSchema,)
def get_job_by_id(
    job_id: int,
    db: Session = Depends(get_db),
):
    return JobService.get_job_by_id(
        db=db,
        job_id=job_id,
    )


# update API
@router.put("/{job_id}")
def update_job(
    job_id: int,
    job: UpdateJobSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "HR"),
    ),
):
    return JobService.update_job(
        db=db,
        job_id=job_id,
        job_data=job,
    )

# Delete API 
@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "HR"),
    ),
):
    return JobService.delete_job(
        db=db,
        job_id=job_id,
    )