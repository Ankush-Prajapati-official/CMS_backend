from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.repositories.candidate_repository import CandidateRepository
from app.schemas.candidate_schema import (
    CreateCandidateSchema,
    UpdateCandidateSchema,
)


class CandidateService:

    # Create Candidate
    @staticmethod
    def create_candidate(db: Session,candidate: CreateCandidateSchema,current_user,):
        # Step 1: Check email   
        existing_candidate = CandidateRepository.get_by_email(
            db=db,
            email=candidate.email,
        )
        if existing_candidate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Candidate email already exists.",
            )

        # Step 2: Check phone
        existing_candidate = CandidateRepository.get_by_phone(
            db=db,
            phone=candidate.phone,
        )

        if existing_candidate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Candidate phone already exists.",
            )

        # Step 3: Create Candidate object
        new_candidate = Candidate(
            first_name=candidate.first_name,
            last_name=candidate.last_name,
            email=candidate.email,
            phone=candidate.phone,
            years_of_experience=candidate.years_of_experience,
            current_company=candidate.current_company,
            current_ctc=candidate.current_ctc,
            expected_ctc=candidate.expected_ctc,
            notice_period=candidate.notice_period,
            current_location=candidate.current_location,
            created_by=current_user.id,
        )

        # Step 4: Save Candidate
        created_candidate = CandidateRepository.create_candidate(
            db=db,
            candidate=new_candidate,
        )

        # Step 5: Return Response
        return {
            "success": True,
            "message": "Candidate created successfully.",
            "candidate_id": created_candidate.id,
        }

    # Get Candidate by ID
    @staticmethod
    def get_candidate_by_id(db: Session,candidate_id: int,):
        candidate = CandidateRepository.get_by_id(
            db=db,
            candidate_id=candidate_id,
        )
        if candidate is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidate not found.",
            )
        return candidate

    # Get All Candidates
    @staticmethod
    def get_all_candidates(
        db: Session,
    ):

        return CandidateRepository.get_all_candidates(
            db=db,
        )

    # Update Candidate
    @staticmethod
    def update_candidate(
        db: Session,
        candidate_id: int,
        candidate_data: UpdateCandidateSchema,
    ): 
         # Step 1: Find Candidate
        candidate = CandidateRepository.get_by_id(
            db=db,
            candidate_id=candidate_id,
        )

        if candidate is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidate not found.",
            )  
             # check email uniqueness    
        if (   # did the user actually change the email?
            candidate_data.email is not None
                # is the new email different from the old email 
               and candidate_data.email != candidate.email):
            #    only then check the database
              existing_candidate = CandidateRepository.get_by_email(db=db,email=candidate_data.email,)
        #  if new updated email someone else already uses then this returns  
              if existing_candidate:
                 raise HTTPException(
                 status_code=status.HTTP_409_CONFLICT,
                 detail="Candidate email already exists.",
               )

        if (candidate_data.phone is not None
            and candidate_data.phone != candidate.phone
           ):
             existing_candidate = CandidateRepository.get_by_phone(
                    db=db,
                   phone=candidate_data.phone,
                 )
             if existing_candidate:
                   raise HTTPException(
                       status_code=status.HTTP_409_CONFLICT,
                       detail="Candidate phone already exists.",
                    )

        # Step 2: Update only provided fields

        if candidate_data.first_name is not None:
            candidate.first_name = candidate_data.first_name

        if candidate_data.last_name is not None:
            candidate.last_name = candidate_data.last_name

        if candidate_data.email is not None:
            candidate.email = candidate_data.email

        if candidate_data.phone is not None:
            candidate.phone = candidate_data.phone

        if candidate_data.years_of_experience is not None:
            candidate.years_of_experience = candidate_data.years_of_experience

        if candidate_data.current_company is not None:
            candidate.current_company = candidate_data.current_company

        if candidate_data.current_ctc is not None:
            candidate.current_ctc = candidate_data.current_ctc

        if candidate_data.expected_ctc is not None:
            candidate.expected_ctc = candidate_data.expected_ctc

        if candidate_data.notice_period is not None:
            candidate.notice_period = candidate_data.notice_period

        if candidate_data.current_location is not None:
            candidate.current_location = candidate_data.current_location

        if candidate_data.status is not None:
            candidate.status = candidate_data.status

        # Step 3: Save
        updated_candidate = CandidateRepository.update_candidate(
            db=db,
            candidate=candidate,
        )

        # Step 4: Return
        return {
            "success": True,
            "message": "Candidate updated successfully.",
            "candidate_id": updated_candidate.id,
        }

    # Delete Candidate
    @staticmethod
    def delete_candidate(db: Session,candidate_id: int,):
        candidate = CandidateRepository.get_by_id(
            db=db,
            candidate_id=candidate_id,
        )
        if candidate is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidate not found.",
            )

        CandidateRepository.delete_candidate(
            db=db,
            candidate=candidate,
        )

        return {
            "success": True,
            "message": "Candidate deleted successfully.",
        }