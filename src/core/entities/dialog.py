from datetime import datetime

from pydantic import BaseModel


class Dialog(BaseModel):
    user_id: int
    user_message: str
    chatbot_message: str
    created_at: datetime
