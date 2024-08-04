from typing import List
from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.utils.validators import check_all_empty
from app.schemas.user_schema import UserBase


class BoardCreate(BaseModel):
    name: str = Field(default=..., description="게시판 이름", max_length=30)
    public: bool = Field(default=..., description="게시판 공개 여부")


class BoardPublic(BoardCreate):
    id: int = Field(default=..., description="게시판 ID")
    count: int = Field(default=..., description="게시판 내 게시글 개수")
    user_id: int = Field(default=..., description="게시판 생성한 유저 ID")
    create_date: datetime = Field(default=..., description="게시판이 생성된 시각")
    user_info: UserBase = Field(default=..., description="게시판 생성한 유저 정보")

    class Config:
        from_attributes = True


class BoardUpdate(BaseModel):
    name: str | None = Field(default=None, description="게시판 이름", max_length=30)
    public: bool | None = Field(default=None, description="게시판 공개 여부")

    validator = model_validator(mode="before")(check_all_empty)


class BoardList(BaseModel):
    page: int = Field(default=..., description="현재 페이지 번호")
    limit: int = Field(default=..., description="페이지 당 게시판 수")
    board_list: List[BoardPublic] | None = Field(
        default=None, title="접근 가능한 게시판 목록"
    )
