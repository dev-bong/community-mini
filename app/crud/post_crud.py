from typing import List
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import Post
from app.schemas.post_schema import PostCreate, PostUpdate
from app.utils import time


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
    post.update_date = time.now_datetime()

    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)

    return post


def delete_post(db_session: Session, post: Post) -> None:
    """
    게시글 삭제 (hard delete)
    """
    db_session.delete(post)
    db_session.commit()


def get_posts_in_board(
    db_session: Session, board_id: int, limit: int, cursor: datetime | None = None
) -> List[Post] | None:
    """
    게시판 내의 게시글들을 cursor pagining 하여 리턴 (최신 게시글 순서로..)
    """
    # 게시판 내 게시글들
    statement = select(Post).filter_by(board_id=board_id)

    if cursor:
        # cursor보다 생성시간이 늦은 아이템들
        statement = statement.filter(Post.create_date < cursor)

    # create_date 역순으로 정렬, limite 적용
    statement = statement.order_by(Post.create_date.desc()).limit(limit)

    posts = db_session.execute(statement).scalars().all()
    return posts
