from typing import Annotated

from fastapi import Depends, HTTPException, Path
from starlette import status
from sqlalchemy.orm import Session

from app.crud import board_crud, post_crud
from app.models import Board, Post
from app.api.deps.db_dep import DatabaseDep

# 게시판 ID 타입 : path parameter 용도
board_id = Annotated[int, Path(default=..., description="게시판 ID")]
# 게시글 ID 타입 : path parameter 용도
post_id = Annotated[int, Path(default=..., description="게시글 ID")]


def get_target_board(db_session: DatabaseDep, board_id: board_id) -> Board:
    """
    수정, 삭제, 읽기의 타겟인 게시판 가져오기
    """
    board = board_crud.get_board_by_id(db_session=db_session, id=board_id)
    if not board:  # 존재하지 않는 ID인 경우
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 게시판입니다.",
        )

    return board


def get_target_post(db_session: DatabaseDep, post_id: post_id) -> Post:
    """
    수정, 삭제, 읽기의 타겟인 게시글 가져오기
    """
    post = post_crud.get_post_by_id(db_session=db_session, id=post_id)
    if not post:  # 존재하지 않는 ID인 경우
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 게시글입니다.",
        )

    return post


TargetBoard = Annotated[Board, Depends(get_target_board)]
TargetPost = Annotated[Post, Depends(get_target_post)]


def check_unique_name(db_session: Session, name: str) -> None:
    """
    게시판 이름 중복 체크
    """
    board = board_crud.get_board_by_name(db_session=db_session, name=name)
    if board:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 존재하는 게시판 이름입니다.",
        )


def check_access_right(req_user_id: int, target: Board | Post) -> None:
    """
    요청 사용자와 게시판(or 게시글) 생성 사용자가 일치하는지 체크
    """
    if req_user_id != target.user_id:
        rsc_type = "게시판" if isinstance(target, Board) else "게시글"
        rsc_name = target.name if rsc_type == "게시판" else target.title
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"해당 '{rsc_name}' {rsc_type}에 접근 권한이 없습니다.",
        )


def check_relation(board: Board, post: Post) -> None:
    """
    게시판과 게시글이 참조 관계인지 체크
    """
    if board.id != post.board_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{board.name} 게시판에 해당 게시글이 존재하지 않습니다.",
        )
