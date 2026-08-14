from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    @staticmethod
    def create_user(db: Session,user: User,) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_by_id(db: Session,user_id: int,) -> User | None:
        statement = select(User).where(User.id == user_id)
        result = db.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    def get_by_email(db: Session,email: str,) -> User | None:
        statement = select(User).where(User.email == email)
        result = db.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    def get_all_users(db: Session,) -> list[User]:
        statement = select(User)
        result = db.execute(statement)
        return result.scalars().all()

    @staticmethod
    def get_by_phone( db: Session,phone: str,) -> User | None:
        statement = select(User).where(User.phone == phone)
        result = db.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    def update_user(db: Session,user: User,) -> User:
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session,user: User,) -> None:
        db.delete(user)
        db.commit()


    # Find user by reset password token
    @staticmethod
    def get_by_reset_token(db: Session,token: str,) -> User | None:
        return db.scalars(
            select(User).where(User.reset_password_token == token)).first()