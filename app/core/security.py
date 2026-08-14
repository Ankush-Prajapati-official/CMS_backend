from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils.jwt import verify_access_token
from fastapi import HTTPException, status

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"      #tells swagger UI that users can obtain token from this endpoint
)


def get_current_user(
    token: str = Depends(oauth2_scheme),  # Extracts the JWT from the Authorization: Bearer <token> header.
    db: Session = Depends(get_db),
 ):
    payload = verify_access_token(token)

    user_id = payload.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token."
        )
    current_user = UserRepository.get_by_id(
        db=db,
        user_id=user_id,
    )
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found."
        )
    return current_user

# Authorization 
def require_roles(*allowed_roles):

    def role_checker(
        current_user: User = Depends(get_current_user),
    ):
        if current_user.role.name not in allowed_roles:
          raise HTTPException(
               status_code=status.HTTP_403_FORBIDDEN,
               detail="You do not have permission to perform this action.",
            )
        return current_user

    return role_checker