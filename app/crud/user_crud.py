from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import User
from app.schemas.user_schema import UserCreate
from app.core.security import get_password_hash


def get_user_by_email(db_session: Session, email: str) -> User | None:
    statement = select(User).filter_by(email=email)
    user = db_session.execute(statement).scalar_one_or_none()
    return user


def create_user(db_session: Session, user_create: UserCreate) -> User:
    user = User(
        email=user_create.email,
        password=get_password_hash(user_create.password),
        full_name=user_create.full_name,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user
