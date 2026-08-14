from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from fastapi import HTTPException, status
from app.schemas.user_schema import (CreateUserSchema,UpdateUserSchema)
from app.utils.password import (hash_password,verify_password,)
from app.utils.jwt import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from app.models.role import Role
from app.schemas.auth_schema import ChangePasswordSchema,ForgotPasswordSchema,ResetPasswordSchema
from datetime import datetime, timedelta, timezone
import secrets
from app.repositories.refreshToken_repository import RefreshTokenRepository
from app.models.refresh_token import RefreshToken


class AuthService:

#   creation Logic for user

    @staticmethod
    def create_user(
        db: Session,
        user: CreateUserSchema,
      ):
        # Step 1: find user by email
        existing_user = UserRepository.get_by_email(
            db,
            user.email
        )
        if existing_user:
          
         raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
             detail="Email already registered."
    )
#  if email not found continue  
         # Step 2: Check phone
        if user.phone:
             existing_phone = UserRepository.get_by_phone(
                 db,
                user.phone,
            )

             if existing_phone:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Phone already registered.",
                )

    # Step 3: Validate role
        role = db.get(Role, user.role_id)

        if role is None:
           raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found.",
        )

        
        # Step 4:  if email is already not registered Hash the password
        hashed_password = hash_password(user.password)

        # Step 5: Create SQLAlchemy User object model
        # here we are maping to create SQL model which is use to represent a database table 
        new_user = User(
            first_name=user.first_name,   #left belong to User Model and right side belong to the pydantic schema from Schema auth model 
            last_name=user.last_name,
            email=user.email,
            password=hashed_password,
            phone=user.phone,
            role_id=user.role_id,
        )

        # Step 4: Save to database
        created_user = UserRepository.create_user(
            db,
            new_user
        )

        # Step 5: Return response
        return {
            "success": True,
            "message": "User created successfully by admin.",
            "user_id": created_user.id,
            "email": created_user.email,
        }

    
# Login Logic

    @staticmethod
    def login(db: Session,form_data: OAuth2PasswordRequestForm,):
    # Step 1: Find user by email
     existing_user = UserRepository.get_by_email(
          db=db,
          email=form_data.username,
        )

     if not existing_user:
          raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED,
             detail="Invalid email or password.",
            )

    # Step 2: Check whether account is active
     if not existing_user.is_active:
          raise HTTPException(
              status_code=status.HTTP_403_FORBIDDEN,
              detail="User account is inactive.",
           )

    # Step 3: Verify password
     password_match = verify_password(
         form_data.password,
         existing_user.password,
       )

     if not password_match:
          raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED,
             detail="Invalid email or password.",
           )

    # Step 4: Create access token
     access_token = create_access_token(
         {
            "user_id": existing_user.id,
            "email": existing_user.email,
            "role": existing_user.role.name,
         }
      )

    # Step 5: Generate refresh token
     refresh_token_value = secrets.token_urlsafe(64)

    # Step 6: Set refresh token expiry
     refresh_token_expiry = (datetime.now(timezone.utc) + timedelta(days=7))

    # Step 7: Create RefreshToken object
     new_refresh_token = RefreshToken(
         user_id=existing_user.id,
         token=refresh_token_value,
         expires_at=refresh_token_expiry,
       )

    # Step 8: Save refresh token
     RefreshTokenRepository.create_token(
         db=db,
         refresh_token=new_refresh_token,
      )

    # Step 9: Return both tokens
     return {
        "success": True,
        "message": "Login successful.",
        "access_token": access_token,
        "refresh_token": refresh_token_value,
        "token_type": "bearer",
    }


    @staticmethod
    def update_profile(db: Session,current_user: User,user_data: UpdateUserSchema,):
    # Update only the fields provided by the user
       if user_data.first_name is not None:
          current_user.first_name = user_data.first_name

       if user_data.last_name is not None:
           current_user.last_name = user_data.last_name

       if user_data.phone is not None:
           current_user.phone = user_data.phone

       updated_user = UserRepository.update_user(
             db=db,
             user = current_user
         )

       return {
          "success": True,
          "message": "Profile updated successfully.",
          "user": {
              "id": updated_user.id,
              "first_name": updated_user.first_name,
              "last_name": updated_user.last_name,
              "email": updated_user.email,
              "phone": updated_user.phone,
              "role_name": updated_user.role.name,
              "is_active": updated_user.is_active,
               "created_at": updated_user.created_at,
               "updated_at": updated_user.updated_at,
            },
        }

# changing user password
    @staticmethod
    def change_password(db: Session,current_user: User,password_data: ChangePasswordSchema,):
    # Step 1: Verify old password
       if not verify_password(
            password_data.old_password,
            current_user.password,
      ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect.",
        )
    # Step 2: Hash new password
       new_hashed_password = hash_password(
           password_data.new_password
         )
    # Step 3: Update password
       current_user.password = new_hashed_password
    # Step 4: Save through repository
       UserRepository.update_user(
           db=db,
           user=current_user,
        )
    # Step 5: Return success response
       return {
          "success": True,
          "message": "Password changed successfully.",
        }


#  Forgot password
    @staticmethod
    def forgot_password(db: Session,data: ForgotPasswordSchema,):
    # Step 1: Find user by email
      user = UserRepository.get_by_email(
           db=db,
           email=data.email,
       )
      if user is None:
           raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND,
              detail="User with this email does not exist.",
           )
    # Step 2: Generate secure reset token
      reset_token = secrets.token_urlsafe(32)
    # Step 3: Set token expiry
      expiry_time = datetime.now(timezone.utc) + timedelta(minutes=15)
    # Step 4: Store token and expiry in user
      user.reset_password_token = reset_token
      user.reset_password_token_expires = expiry_time
    # Step 5: Save through repository
      UserRepository.update_user(
          db=db,
          user=user,
        )
    # Step 6: Return response
      return {
          "success": True,
          "message": "Password reset token generated successfully.",
          "reset_token": reset_token,
        }

#  RESET password
    @staticmethod
    def reset_password(db: Session,data: ResetPasswordSchema,):
    # Step 1: Find user using reset token
      user = UserRepository.get_by_reset_token(
           db=db,
           token=data.token,
        )
      if user is None:
            raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST,
               detail="Invalid reset token.",
            )
    # Step 2: Check whether token has expired
      if (user.reset_password_token_expires is None or user.reset_password_token_expires < datetime.now(timezone.utc)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired.",
        )
    # Step 3: Hash the new password
      user.password = hash_password(
          data.new_password
       )
    # Step 4: Clear reset token after successful use
      user.reset_password_token = None
      user.reset_password_token_expires = None
    # Step 5: Save changes
      UserRepository.update_user(
           db=db,
          user=user,
       )
    # Step 6: Return response
      return {
        "success": True,
        "message": "Password reset successfully.",
    }

# refresh access token 
    @staticmethod
    def refresh_access_token(db: Session,refresh_token: str,):
    # Step 1: Find refresh token in database
     stored_token = RefreshTokenRepository.get_by_token(
          db=db,
          token=refresh_token,
       )

     if stored_token is None:
          raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED,
             detail="Invalid refresh token.",
           )

    # Step 2: Check if token has been revoked
     if stored_token.revoked_at is not None:
          raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED,
             detail="Refresh token has been revoked.",
           )

    # Step 3: Check token expiry
     if stored_token.expires_at < datetime.now(timezone.utc):
          raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED,
             detail="Refresh token has expired.",
           )

     # Step 4: Find the user
     user = UserRepository.get_by_id(
          db=db,
         user_id=stored_token.user_id,
        )

     if user is None:
         raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED,
             detail="User not found.",
            )

    # Step 5: Check whether user is active
     if not user.is_active:
         raise HTTPException(
             status_code=status.HTTP_403_FORBIDDEN,
             detail="User account is inactive.",
           )

    # Step 6: Generate new access token
     access_token = create_access_token(
         {
            "user_id": user.id,
            "email": user.email,
            "role": user.role.name,
         }
      )

     # Step 7: Return new access token
     return {
          "success": True,
          "message": "Access token refreshed successfully.",
         "access_token": access_token,
         "token_type": "bearer",
       }


#  Logout 
    @staticmethod
    def logout(db: Session,refresh_token: str,):
    # Step 1: Find refresh token
     stored_token = RefreshTokenRepository.get_by_token(
         db=db,
         token=refresh_token,
       )

     if stored_token is None:
          raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail="Refresh token not found.",
          )

    # Step 2: Check if already revoked
     if stored_token.revoked_at is not None:
         raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST,
             detail="User is already logged out.",
          )

    # Step 3: Revoke token
     RefreshTokenRepository.revoke_token(
         db=db,
         refresh_token=stored_token,
       )

    # Step 4: Return response
     return {
         "success": True,
         "message": "Logout successful.",
       }
      



