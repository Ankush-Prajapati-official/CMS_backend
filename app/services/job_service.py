from sqlalchemy.orm import Session
from app.models.job import Job
from app.models.user import User
from app.schemas.job_schema import (CreateJobSchema,UpdateJobSchema,)
from app.repositories.job_repository import JobRepository
from fastapi import HTTPException, status


class JobService:

# create job 

    @staticmethod
    def create_job(
        db: Session,
        job: CreateJobSchema,
        current_user: User,
    ):
        new_job = Job(
            title=job.title,
            description=job.description,
            location=job.location,
            employment_type=job.employment_type,
            experience=job.experience,
            salary=job.salary,

            # Automatically set by backend
            created_by=current_user.id,
        )
        #save to database
        created_job = JobRepository.create_job(
            db = db,
            job = new_job
        )

        #return response
        return{
            "success": True,
            "message" : "Job created successfully",
            "job_id": created_job.id,
            }


#  get job by id 
    @staticmethod
    def get_job_by_id(
       db: Session,
       job_id: int,
    ):
        job = JobRepository.get_by_id(
             db=db,
             job_id=job_id,
        )

        if job is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found.",
            )

        return job

    @staticmethod
    def get_all_jobs(
        db: Session,
   ):
        jobs = JobRepository.get_all_jobs(
              db=db,
        )

        return jobs


#  update the job
    @staticmethod
    def update_job(
       db: Session,
       job_id: int,
       job_data: UpdateJobSchema,
    ):
     # Step 1: Fetch the job
        job = JobRepository.get_by_id(
            db=db,
            job_id=job_id,
        )

       # Step 2: Check if job exists
        if job is None:
           raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found.",
            )

    # Step 3: Update only the provided fields
        if job_data.title is not None:
             job.title = job_data.title

        if job_data.description is not None:
             job.description = job_data.description

        if job_data.location is not None:
             job.location = job_data.location

        if job_data.employment_type is not None:
             job.employment_type = job_data.employment_type

        if job_data.experience is not None:
             job.experience = job_data.experience

        if job_data.salary is not None:
             job.salary = job_data.salary

        if job_data.status is not None:
             job.status = job_data.status

    # Step 4: Save changes
        updated_job = JobRepository.update_job(
           db=db,
           job=job,
        )

    # Step 5: Return response
        return {
             "success": True,
             "message": "Job updated successfully.",
             "job_id": updated_job.id,
            }


# Deleting job
    @staticmethod
    def delete_job(
         db: Session,
         job_id: int,
    ):
    # Step 1: Find the job
       job = JobRepository.get_by_id(
            db=db,
            job_id=job_id,
        )

    # Step 2: Check if it exists
       if job is None:
             raise HTTPException(
                 status_code=status.HTTP_404_NOT_FOUND,
                 detail="Job not found.",
               )

    # Step 3: Delete
       JobRepository.delete_job(
            db=db,
           job=job,
        )
    # Step 4: Return response
       return {
           "success": True,
            "message": "Job deleted successfully.",
        }