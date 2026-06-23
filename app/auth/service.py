from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User
from app.auth.schemas import UserCreate
from app.auth.security import hash_password, verify_password


def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_email(db: Session, email: str):
    return db.scalar(select(User).where(User.email == email))


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user