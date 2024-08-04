from typing import Any

from fastapi import APIRouter, HTTPException, Path
from starlette import status

from app.schemas import post_schema, common_schema
from app.api.deps.db_dep import DatabaseDep
from app.api.deps.user_dep import CurrentUser, CurrentUserOptional
from app.api.deps.extra_dep import (
    TargetBoard,
    TargetPost,
    check_access_right,
    check_relation,
)
from app.crud import post_crud

router = APIRouter()


@router.post(
    "",
    response_model=post_schema.PostPublic,
    status_code=status.HTTP_201_CREATED,
    summary="게시글 생성",
    description="게시판에 새로운 게시글 생성",
)
def create_post(
    db_session: DatabaseDep,
    current_user: CurrentUser,
    board: TargetBoard,
    post_info: post_schema.PostCreate,
) -> Any:
    new_post = post_crud.create_post(
        db_session=db_session,
        post_create=post_info,
        user_id=current_user.id,
        board_id=board.id,
    )

    return new_post


@router.patch(
    "/{post_id}",
    response_model=post_schema.PostPublic,
    status_code=status.HTTP_201_CREATED,
    summary="게시글 수정",
    description="내가 쓴 게시글 수정",
)
def update_post(
    db_session: DatabaseDep,
    current_user: CurrentUser,
    board: TargetBoard,
    post: TargetPost,
    post_info: post_schema.PostUpdate,
) -> Any:
    check_relation(board=board, post=post)
    check_access_right(req_user_id=current_user.id, target=post)

    updated_post = post_crud.update_post(
        db_session=db_session, post=post, post_update=post_info
    )

    return updated_post


@router.delete(
    "/{post_id}",
    response_model=common_schema.Message,
    summary="게시글 삭제",
    description="내가 쓴 게시글 삭제",
)
def delete_post(
    db_session: DatabaseDep,
    current_user: CurrentUser,
    board: TargetBoard,
    post: TargetPost,
) -> Any:
    check_relation(board=board, post=post)
    check_access_right(req_user_id=current_user.id, target=post)

    post_title = post.title
    post_crud.delete_post(db_session=db_session, post=post)

    return {"message": f"{post_title} 게시글이 삭제되었습니다."}


@router.get(
    "/{post_id}",
    response_model=post_schema.PostPublic,
    summary="게시글 읽기",
    description="게시글 읽기",
)
def read_post(
    current_user: CurrentUserOptional,
    board: TargetBoard,
    post: TargetPost,
) -> Any:
    check_relation(board=board, post=post)

    # 게시판이 private일 때
    if board.public is False:
        # 로그인 상태가 아닌 경우
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"해당 '{board.name}' 게시판은 private 상태입니다. 로그인 후 다시 시도해보세요.",
            )
        check_access_right(req_user_id=current_user.id, target=board)

    return post
