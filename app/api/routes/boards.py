from typing import Any
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path
from starlette import status

from app.schemas import board_schema, common_schema
from app.api.deps import DatabaseDep, CurrentUser, CurrentUserOptional
from app.crud import board_crud

router = APIRouter()

# 게시판 ID 타입 : path parameter 용도
board_id = Annotated[int, Path(default=..., description="게시판 ID")]


@router.post(
    "/",
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
    # 게시판 이름 중복 체크
    board = board_crud.get_board_by_name(db_session=db_session, name=board_info.name)
    if board:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 존재하는 게시판 이름입니다.",
        )

    new_board = board_crud.create_board(
        db_session=db_session, board_create=board_info, user_id=current_user.id
    )

    return new_board


@router.patch(
    "/{id}",
    response_model=board_schema.BoardPublic,
    status_code=status.HTTP_201_CREATED,
    summary="게시판 수정",
    description="내가 생성한 게시판 수정하기",
)
def update_board(
    db_session: DatabaseDep,
    current_user: CurrentUser,
    board_info: board_schema.BoardUpdate,
    id: board_id,
) -> Any:
    board = board_crud.get_board_by_id(db_session=db_session, id=id)
    # 수정하려는 게시판을 생성한 유저 ID와 요청을 보낸 유저 ID가 다른 경우
    if board.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="다른 유저가 생성한 게시판은 수정할 수 없습니다.",
        )

    # 게시판의 이름을 수정하려는 경우 이름 중복 체크
    if (
        board_info.name and board_info.name != board.name
    ):  # 수정하려는 게시판은 중복 체크 제외
        name_board = board_crud.get_board_by_name(
            db_session=db_session, name=board_info.name
        )
        if name_board:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 존재하는 게시판 이름입니다.",
            )

    updated_board = board_crud.update_board(
        db_session=db_session, board=board, board_update=board_info
    )

    return updated_board


@router.delete(
    "/{id}",
    response_model=common_schema.Message,
    summary="게시판 삭제",
    description="게시판 삭제",
)
def delete_board(
    db_session: DatabaseDep,
    current_user: CurrentUser,
    id: board_id,
) -> Any:
    board = board_crud.get_board_by_id(db_session=db_session, id=id)
    if not board:  # 이미 삭제되었거나 존재하지 않는 ID인 경우
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 게시판입니다.",
        )
    # 삭제하려는 게시판을 생성한 유저 ID와 요청을 보낸 유저 ID가 다른 경우
    if board.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="다른 유저가 생성한 게시판은 수정할 수 없습니다.",
        )

    board_name = board.name
    board_crud.delete_board(db_session=db_session, board=board)

    return {"message": f"{board_name} 게시판이 삭제되었습니다."}


@router.get(
    "/{id}",
    response_model=board_schema.BoardPublic,
    summary="게시판 읽기",
    description="게시판 정보 읽기",
)
def read_board(
    db_session: DatabaseDep,
    current_user: CurrentUserOptional,
    id: board_id,
) -> Any:
    board = board_crud.get_board_by_id(db_session=db_session, id=id)
    if not board:  # 이미 삭제되었거나 존재하지 않는 ID인 경우
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 게시판입니다.",
        )

    # 게시판이 private일 때
    if board.public is False:
        # 로그인 상태가 아닌 경우
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="해당 게시판은 private 상태입니다. 로그인 후 다시 시도해보세요.",
            )
        # 읽기 요청 사용자와 게시판을 생성한 사용자가 일치하지 않는 경우
        elif current_user.id != board.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="해당 게시판에 접근 권한이 없습니다.",
            )

    return board
