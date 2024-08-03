from typing import Any
from typing import Annotated

from fastapi import APIRouter, HTTPException, Response, Cookie
from starlette import status

from app.api.deps import DatabaseDep, PasswordFormDep
from app.crud import user_crud
from app.core import security
from app.schemas import common_schema

router = APIRouter()


@router.post(
    "/login",
    response_model=common_schema.Message,
    status_code=status.HTTP_201_CREATED,
    summary="로그인",
    description="로그인하여 세션 생성",
)
def login_user(
    db_session: DatabaseDep, form_data: PasswordFormDep, response: Response
) -> Any:
    user = user_crud.authenticate(
        db_session=db_session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="잘못된 닉네임 또는 비밀번호입니다.",
        )

    # redis에 세션 생성
    session_id = security.create_session(user_id=user.id)
    # 쿠키에 세션 id 저장
    response.set_cookie(key="session_id", value=session_id, httponly=True)

    return {"message": "로그인이 완료되었습니다."}


@router.post(
    "/logout",
    response_model=common_schema.Message,
    status_code=status.HTTP_201_CREATED,
    summary="로그아웃",
    description="현재 세션 삭제",
)
def logout_user(
    response: Response, session_id: Annotated[str | None, Cookie()] = None
) -> Any:
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

    # redis에서 세션 삭제
    security.delete_session(session_id=session_id)
    # 쿠키에서 세션 id 삭제
    response.delete_cookie(key="session_id", httponly=True)

    return {"message": "로그아웃이 완료되었습니다."}
