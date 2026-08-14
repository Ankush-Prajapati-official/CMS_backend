import os
import shutil
import uuid
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from app.models.resume import Resume
from app.repositories.resume_repository import ResumeRepository
from app.repositories.candidate_repository import CandidateRepository


class ResumeService:

    @staticmethod
    def upload_resume(
        db: Session,
        candidate_id:int,
        file: UploadFile,
    ):
        #    Check candidate exists
        candidate = CandidateRepository.get_by_id(
                  db=db,
                  candidate_id=candidate_id,
            )

        if candidate is None:
            raise HTTPException(
                  status_code=status.HTTP_404_NOT_FOUND,
                   detail="Candidate not found.",
        )
        # Allow only PDF files
        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed.",
            )
        # Extract file extension
        file_extension = os.path.splitext(file.filename)[1]
        # Generate unique filename
        stored_file_name = f"{uuid.uuid4()}{file_extension}"
        # Create upload directory if it doesn't exist
        upload_dir = "uploads/resumes"
        os.makedirs(upload_dir, exist_ok=True)
        # Create full file path
        file_path = os.path.join(
            upload_dir,
            stored_file_name,
        )
        # Save the uploaded file
        try:
            with open(file_path, "wb") as buffer:    #wb -> write binary
                shutil.copyfileobj(file.file, buffer)

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload resume.",
            )

        # Check if the user already has a resume
        existing_resume = ResumeRepository.get_by_candidate_id(
            db=db,
            candidate_id=candidate_id,
        )
        if existing_resume:
    # Delete old resume file if it exists
          if os.path.exists(existing_resume.file_path):
             os.remove(existing_resume.file_path)

    # Update existing resume details
          existing_resume.file_name = file.filename
          existing_resume.stored_file_name = stored_file_name
          existing_resume.file_path = file_path

          updated_resume = ResumeRepository.update_resume(
                 db=db,
                 resume=existing_resume,
            )

          return {
                 "success": True,
                 "message": "Resume updated successfully.",
                "resume_id": updated_resume.id,
           }

    # User is uploading a resume for the first time
        new_resume = Resume(
             file_name=file.filename,
             stored_file_name=stored_file_name,
             file_path=file_path,
              candidate_id=candidate_id,
        )

        created_resume = ResumeRepository.create_resume(
             db=db,
            resume=new_resume,
        )

        return {
                "success": True,
                 "message": "Resume uploaded successfully.",
                  "resume_id": created_resume.id,
                }

# if candidate wants to delete his resume 
    @staticmethod
    def delete_resume(
        db: Session,
        candidate_id: int,
     ):
        candidate = CandidateRepository.get_by_id(
            db=db,
             candidate_id=candidate_id,
          )

        if candidate is None:
           raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND,
              detail="Candidate not found.",
           )
        existing_resume = ResumeRepository.get_by_candidate_id(
                db=db,
                candidate_id=candidate_id,
         )
        if existing_resume is None:
                  raise HTTPException(
                       status_code=status.HTTP_404_NOT_FOUND,
                       detail="Resume not found.",
         )

        if os.path.exists(existing_resume.file_path):
             os.remove(existing_resume.file_path)

        ResumeRepository.delete_resume(
                  db=db,
                  resume=existing_resume,
        )
        return {
            "success":True,
            "message": "Resume deleted successfully"
        }