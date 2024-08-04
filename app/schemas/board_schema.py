from typing import Any

from pydantic import BaseModel, Field, model_validator


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

    # 모든 필드가 비어있는 경우 체크
    @model_validator(mode="before")
    @classmethod
    def check_all_empty(cls, data: Any) -> Any:
        count = 0
        for attr_name, attr_value in enumerate(data):
            if attr_value is not None:
                count += 1

        if count == 0:
            raise ValueError("적어도 하나의 필드에는 값을 입력해야 합니다.")

        return data
