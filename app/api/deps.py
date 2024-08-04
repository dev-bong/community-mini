from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import Depends, Cookie, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.core.db import SessionLocal
from app.core import security
from app.crud import user_crud
from app.models import User


def get_db():  # 데이터베이스 세션 관리
    db = SessionLocal()
    try:
        yield db  # 세션 생성
    finally:
        db.close()  # 세션 종료


DatabaseDep = Annotated[Session, Depends(get_db)]
PasswordFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


def get_current_user(
    db_session: DatabaseDep, session_id: Annotated[str | None, Cookie()] = None
) -> User:
    """
    로그인 상태에서만 사용할 수 있는 API에 사용 (Create, Update, Delete ..)
    - 현재 로그인 중인 유저 정보를 리턴 (리턴하지 못하면 에러 발생)
    """
    if not session_id:  # 쿠키에 세션 id X
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="현재 로그인 상태가 아닙니다.",
        )

    user_id = security.get_session(session_id=session_id)
    if not user_id:  # redis에 세션 id X
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="유효하지 않거나 이미 만료된 세션입니다.",
        )

    user = user_crud.get_user_by_id(db_session=db_session, id=user_id)
    if not user:  # db에 유저 id X (탈퇴한 유저의 경우?(아직 api 없음))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 유저의 세션입니다.",
        )

    return user


def get_curret_user_optional(
    db_session: DatabaseDep, session_id: Annotated[str | None, Cookie()] = None
) -> User | None:
    """
    로그인 하지 않은 상태에서도 사용할 수 있는 API에 사용 (Get)
    - 유저 정보 리턴할 수 있으면 하고, 안되면 None 리턴
    """
    if session_id:
        user_id = security.get_session(session_id=session_id)
        if user_id:
            user = user_crud.get_user_by_id(db_session=db_session, id=user_id)
            if user:
                return user
    return None


CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentUserOptional = Annotated[User | None, Depends(get_curret_user_optional)]
