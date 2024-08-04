from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import Post, Board
from app.schemas.post_schema import PostCreate, PostUpdate


def create_post(
    db_session: Session, post_create: PostCreate, user_id: int, board_id: int
) -> Post:
    """
    게시글 생성
    """
    post = Post(
        title=post_create.title,
        content=post_create.content,
        user_id=user_id,
        board_id=board_id,
    )

    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)

    # 게시판 게시글 수 업데이트
    post.board.count += 1
    db_session.add(post.board)
    db_session.commit()

    return post


def get_post_by_id(db_session: Session, id: int) -> Post | None:
    """
    ID로 게시글 읽기
    """
    return db_session.get(Post, id)


def update_post(db_session: Session, post: Post, post_update: PostUpdate) -> Post:
    """
    게시글 업데이트
    """
    if post_update.title:
        post.title = post_update.title
    if post_update.content:
        post.content = post_update.content

    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)

    return post


def delete_post(db_session: Session, post: Post) -> None:
    """
    게시글 삭제 (hard delete)
    """
    post.board.count -= 1  # 게시판 게시글 수 업데이트
    db_session.add(post.board)
    db_session.delete(post)
    db_session.commit()
