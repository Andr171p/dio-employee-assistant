from typing import Literal

from pydantic import BaseModel


class ChatMessage(BaseModel):
    type: Literal["human", "dio"]
    content: str
