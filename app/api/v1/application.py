from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.core.security import require_roles
from app.models.user import User
from app.schemas.application_schema import (CreateApplicationSchema,UpdateApplicationSchema,ApplicationResponseSchema,)
from app.services.application_service import ApplicationService


router = APIRouter(
    prefix="/api/v1/applications",
    tags=["Applications"],
)


# Create Application
@router.post("/",status_code=status.HTTP_201_CREATED,)
def create_application(
    application: CreateApplicationSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "HR")
    ),
):
    return ApplicationService.create_application(
        db=db,
        application=application,
        current_user=current_user,
    )

# Get All Applications
@router.get("/",response_model=list[ApplicationResponseSchema],)
def get_all_applications(
    db: Session = Depends(get_db),
):
    return ApplicationService.get_all_applications(
        db=db,
    )

# Get Application by ID
@router.get("/{application_id}",response_model=ApplicationResponseSchema,)
def get_application_by_id(
    application_id: int,
    db: Session = Depends(get_db),
):
    return ApplicationService.get_application_by_id(
        db=db,
        application_id=application_id,
    )

# Update Application Status
@router.put("/{application_id}/status",)
def update_application_status(
    application_id: int,
    status_data: UpdateApplicationSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "HR")
    ),
):
    return ApplicationService.update_application_status(
        db=db,
        application_id=application_id,
        status_data=status_data,
    )

# Delete Application
@router.delete("/{application_id}",)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "HR")
    ),
):
    return ApplicationService.delete_application(
        db=db,
        application_id=application_id,
    )