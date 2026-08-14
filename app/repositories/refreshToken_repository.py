from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.refresh_token import RefreshToken
from datetime import datetime, timezone

class RefreshTokenRepository:

    # Create refresh token
    @staticmethod
    def create_token(db: Session,refresh_token: RefreshToken,) -> RefreshToken:
        db.add(refresh_token)
        db.commit()
        db.refresh(refresh_token)
        return refresh_token

    # Find refresh token
    @staticmethod
    def get_by_token(db: Session,token: str,) -> RefreshToken | None:
        return db.scalars(
            select(RefreshToken).where(RefreshToken.token == token)).first()

    # Revoke refresh token
    @staticmethod
    def revoke_token(db: Session,refresh_token: RefreshToken,) -> RefreshToken:
        refresh_token.revoked_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(refresh_token)
        return refresh_token