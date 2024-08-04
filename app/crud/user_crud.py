from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import User
from app.schemas.user_schema import UserCreate
from app.core.security import get_password_hash, verify_password


def get_user_by_email(db_session: Session, email: str) -> User | None:
    """
    이메일로 유저 정보 읽기
    """
    statement = select(User).filter_by(email=email)
    user = db_session.execute(statement).scalar_one_or_none()
    return user


def create_user(db_session: Session, user_create: UserCreate) -> User:
    """
    유저 생성
    """
    user = User(
        email=user_create.email,
        password=get_password_hash(user_create.password),
        full_name=user_create.full_name,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


def authenticate(db_session: Session, email: str, password: str) -> User | None:
    """
    평문 비밀번호와 DB에 저장된 암호화 비밀번호 비교
    """
    user = get_user_by_email(db_session=db_session, email=email)
    if not user or not verify_password(password, user.password):
        return None
    return user


def get_user_by_id(db_session: Session, id: int) -> User | None:
    """
    id로 유저 읽기
    """
    return db_session.get(User, id)
