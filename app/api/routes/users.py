from typing import Any

from fastapi import APIRouter, HTTPException
from starlette import status

from app.schemas import user_schema
from app.api.deps.db_dep import DatabaseDep
from app.crud import user_crud

router = APIRouter()


@router.post(
    "/signup",
    response_model=user_schema.UserPublic,
    status_code=status.HTTP_201_CREATED,
    summary="회원가입",
    description="신규 유저 회원가입",
)
def create_user(db_session: DatabaseDep, user_info: user_schema.UserCreate) -> Any:
    user = user_crud.get_user_by_email(db_session=db_session, email=user_info.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 이메일입니다."
        )
    user = user_crud.create_user(db_session=db_session, user_create=user_info)

    return user
