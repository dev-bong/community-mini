from typing import Optional, List
from typing_extensions import Annotated
from datetime import datetime

from sqlalchemy import String, Text, ForeignKey, TIMESTAMP
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

# * mapped_column() overrides
int_pk = Annotated[int, mapped_column(primary_key=True)]
user_fk = Annotated[int, mapped_column(ForeignKey("user.id", ondelete="CASCADE"))]
board_fk = Annotated[int, mapped_column(ForeignKey("board.id", ondelete="CASCADE"))]
date = Annotated[datetime, mapped_column(TIMESTAMP(timezone=True))]
str30 = Annotated[str, mapped_column(String(30))]
text = Annotated[str, mapped_column(Text)]


class Base(DeclarativeBase):
    pass


class User(Base):  # 사용자 테이블
    __tablename__ = "user"

    id: Mapped[int_pk]
    email: Mapped[str] = mapped_column(unique=True)
    full_name: Mapped[str30]
    join_date: Mapped[date] = mapped_column(insert_default=func.now())
    password: Mapped[str]

    # 유저가 생성한 게시판들
    boards: Mapped[List["Board"]] = relationship(
        back_populates="user", cascade="all, delete"
    )
    # 유저가 쓴 게시글들
    posts: Mapped[List["Post"]] = relationship(
        back_populates="user", cascade="all, delete"
    )


class Board(Base):  # 게시판 테이블
    __tablename__ = "board"

    id: Mapped[int_pk]
    name: Mapped[str30] = mapped_column(unique=True)
    public: Mapped[bool]  # public 여부
    count: Mapped[int]  # 게시판 내 게시글 개수
    create_date: Mapped[date] = mapped_column(insert_default=func.now())
    update_date: Mapped[date] = mapped_column(insert_default=func.now())
    user_id: Mapped[user_fk]

    # 게시판 생성한 유저
    user: Mapped["User"] = relationship(back_populates="boards")
    # 게시판 내 게시글들
    posts: Mapped[List["Post"]] = relationship(
        back_populates="board", cascade="all, delete"
    )


class Post(Base):  # 게시글 테이블
    __tablename__ = "post"

    id: Mapped[int_pk]
    title: Mapped[str30]
    content: Mapped[text]
    create_date: Mapped[date] = mapped_column(insert_default=func.now())
    update_date: Mapped[date] = mapped_column(insert_default=func.now())
    user_id: Mapped[user_fk]
    board_id: Mapped[board_fk]

    # 게시글을 쓴 유저
    user: Mapped["User"] = relationship(back_populates="posts")
    # 게시글이 등록된 게시판
    board: Mapped["Board"] = relationship(back_populates="posts")
