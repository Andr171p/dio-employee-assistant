from typing import Optional

from enum import StrEnum

from pydantic import BaseModel, field_validator, ConfigDict


class Role(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"


class Grade(StrEnum):
    LIKE = "like"
    DISLIKE = "dislike"


class BaseMessage(BaseModel):
    id: int
    role: Role
    chat_id: str | int
    text: str
    grade: Optional[Grade] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    @field_validator("chat_id")
    def validate_chat_id(cls, chat_id: str | int) -> str:
        return str(chat_id)
