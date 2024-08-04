from typing import List
from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.utils.validators import check_all_empty
from app.schemas.user_schema import UserBase


class PostCreate(BaseModel):
    title: str = Field(default=..., description="게시글 제목", max_length=30)
    content: str = Field(default=..., description="게시글 내용")


class PostPublic(PostCreate):
    id: int = Field(default=..., description="게시글 ID")
    user_id: int = Field(default=..., description="게시글 생성한 유저 ID")
    board_id: int = Field(default=..., description="게시글이 속한 게시판 ID")
    create_date: datetime = Field(default=..., description="게시글이 생성된 시각")
    user_info: UserBase = Field(default=..., description="게시글을 쓴 유저 정보")

    class Config:
        from_attributes = True


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, description="게시글 제목", max_length=30)
    content: str | None = Field(default=None, description="게시글 내용")

    validator = model_validator(mode="before")(check_all_empty)


class PostList(BaseModel):
    board_id: int = Field(default=..., description="게시글들이 속한 게시판 ID")
    limit: int = Field(default=..., description="페이지 당 게시글 수")
    post_list: List[PostPublic] | None = Field(
        default=None, title="현재 페이지의 게시글 목록"
    )
