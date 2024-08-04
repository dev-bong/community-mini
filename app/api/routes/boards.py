from typing import Any

from fastapi import APIRouter, HTTPException, Path
from starlette import status

from app.schemas import board_schema, common_schema
from app.api.deps.db_dep import DatabaseDep
from app.api.deps.user_dep import CurrentUser, CurrentUserOptional
from app.api.deps.extra_dep import (
    TargetBoard,
    check_unique_name,
    check_access_right,
)
from app.crud import board_crud

router = APIRouter()


@router.post(
    "",
    response_model=board_schema.BoardPublic,
    status_code=status.HTTP_201_CREATED,
    summary="게시판 생성",
    description="새로운 게시판 생성",
)
def create_board(
    db_session: DatabaseDep,
    current_user: CurrentUser,
    board_info: board_schema.BoardCreate,
) -> Any:
    check_unique_name(db_session=db_session, name=board_info.name)

    new_board = board_crud.create_board(
        db_session=db_session, board_create=board_info, user_id=current_user.id
    )

    return new_board


@router.patch(
    "/{board_id}",
    response_model=board_schema.BoardPublic,
    status_code=status.HTTP_201_CREATED,
    summary="게시판 수정",
    description="내가 생성한 게시판 수정하기",
)
def update_board(
    db_session: DatabaseDep,
    current_user: CurrentUser,
    board_info: board_schema.BoardUpdate,
    board: TargetBoard,
) -> Any:
    check_access_right(req_user_id=current_user.id, target=board)

    # 게시판의 이름을 수정하려는 경우 이름 중복 체크
    if (
        board_info.name and board_info.name != board.name
    ):  # 수정하려는 게시판은 중복 체크 제외
        check_unique_name(db_session=db_session, name=board_info.name)

    updated_board = board_crud.update_board(
        db_session=db_session, board=board, board_update=board_info
    )

    return updated_board


@router.delete(
    "/{board_id}",
    response_model=common_schema.Message,
    summary="게시판 삭제",
    description="내가 생성한 게시판 삭제",
)
def delete_board(
    db_session: DatabaseDep,
    current_user: CurrentUser,
    board: TargetBoard,
) -> Any:
    check_access_right(req_user_id=current_user.id, target=board)

    board_name = board.name
    board_crud.delete_board(db_session=db_session, board=board)

    return {"message": f"{board_name} 게시판이 삭제되었습니다."}


@router.get(
    "/{board_id}",
    response_model=board_schema.BoardPublic,
    summary="게시판 읽기",
    description="게시판 정보 읽기",
)
def read_board(
    current_user: CurrentUserOptional,
    board: TargetBoard,
) -> Any:
    # 게시판이 private일 때
    if board.public is False:
        # 로그인 상태가 아닌 경우
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"해당 '{board.name}' 게시판은 private 상태입니다. 로그인 후 다시 시도해보세요.",
            )
        check_access_right(req_user_id=current_user.id, target=board)

    return board
