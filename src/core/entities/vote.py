from typing import Literal

from pydantic import BaseModel


class Vote(BaseModel):
    message_id: int
    vote_type: Literal["like", "dislike"]
