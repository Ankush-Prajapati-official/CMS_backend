from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.services.auth_service import AuthService
from app.schemas.user_schema import (CreateUserSchema,UserResponseSchema,UpdateUserSchema)
from app.models.user import User
from app.schemas.auth_schema import ChangePasswordSchema,ForgotPasswordSchema,ResetPasswordSchema
from app.schemas.auth_schema import (ChangePasswordSchema,ForgotPasswordSchema,ResetPasswordSchema,RefreshTokenSchema,)


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)

@router.post("/register")
def register(user: CreateUserSchema,db: Session = Depends(get_db),):
    return AuthService.create_user(
        db=db,
        user=user,
    )

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db),):
    return AuthService.login(
        db=db,
        form_data=form_data,
    )

@router.get("/profile",response_model=UserResponseSchema,)
def get_profile(current_user: User = Depends(get_current_user),):
    return {
        "id": current_user.id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "phone": current_user.phone,
        "role_name": current_user.role.name,
        "is_active" : current_user.is_active,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at,
    }

# Update logged-in user's profile

@router.put("/profile")
def update_profile(user_data: UpdateUserSchema,db: Session = Depends(get_db),current_user: User = Depends(get_current_user),):
    return AuthService.update_profile(
        db=db,
        current_user=current_user,
        user_data=user_data,
    )

# change the password 
@router.put("/change-password")
def change_password(
    password_data: ChangePasswordSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AuthService.change_password(
        db=db,
        current_user=current_user,
        password_data=password_data,
    )

# Forgot Password 
@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordSchema,db: Session = Depends(get_db),):
    return AuthService.forgot_password(
        db=db,
        data=data,
    )

# reset password
@router.post("/reset-password")
def reset_password(data: ResetPasswordSchema,db: Session = Depends(get_db),):
    return AuthService.reset_password(
        db=db,
        data=data,
    )

# Refresh Access Token
@router.post("/refresh")
def refresh_token(data: RefreshTokenSchema,db: Session = Depends(get_db),):
    return AuthService.refresh_access_token(
        db=db,
        refresh_token=data.refresh_token,
    )

# Logout
@router.post("/logout")
def logout(data: RefreshTokenSchema,db: Session = Depends(get_db),):
    return AuthService.logout(
        db=db,
        refresh_token=data.refresh_token,
    )
