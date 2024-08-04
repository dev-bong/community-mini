from pydantic import BaseModel, Field, model_validator

from app.utils.validators import check_all_empty


class BoardCreate(BaseModel):
    name: str = Field(default=..., description="게시판 이름", max_length=30)
    public: bool = Field(default=..., description="게시판 공개 여부")


class BoardPublic(BoardCreate):
    id: int = Field(default=..., description="게시판 ID")
    count: int = Field(default=..., description="게시판 내 게시글 개수")
    user_id: int = Field(default=..., description="게시판 생성한 유저 ID")

    class Config:
        from_attributes = True


class BoardUpdate(BaseModel):
    name: str | None = Field(default=None, description="게시판 이름", max_length=30)
    public: bool | None = Field(default=None, description="게시판 공개 여부")

    validator = model_validator(mode="before")(check_all_empty)
