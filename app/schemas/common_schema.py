from pydantic import BaseModel, Field


class Message(BaseModel):
    message: str = Field(default=..., description="메시지")
