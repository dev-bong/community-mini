from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    email: EmailStr = Field(default=..., description="이메일")
    full_name: str | None = Field(
        default="Unknown",
        description="사용자 이름 (입력안할 시 'Unknown'으로 자동 설정)",
        max_length=30,
    )


class UserCreate(UserBase):
    password: str = Field(default=..., description="비밀번호")


class UserPublic(UserBase):
    id: int = Field(default=..., description="유저 ID")

    class Config:
        from_attributes = True
