from pydantic import BaseModel, Field, model_validator

from app.utils.validators import check_all_empty


class PostCreate(BaseModel):
    title: str = Field(default=..., description="게시글 제목", max_length=30)
    content: str = Field(default=..., description="게시글 내용")


class PostPublic(PostCreate):
    id: int = Field(default=..., description="게시글 ID")
    user_id: int = Field(default=..., description="게시글 생성한 유저 ID")
    board_id: int = Field(default=..., description="게시글이 속한 게시판 ID")

    class Config:
        from_attributes = True


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, description="게시글 제목", max_length=30)
    content: str | None = Field(default=None, description="게시글 내용")

    validator = model_validator(mode="before")(check_all_empty)
