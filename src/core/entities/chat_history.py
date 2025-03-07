from typing import List

from pydantic import BaseModel

from src.core.entities import Dialog


class ChatHistory(BaseModel):
    user_id: int
    dialogs: List[Dialog]
