from datetime import datetime

from pydantic import BaseModel


class Dialog(BaseModel):
    user_message: str
    chatbot_message: str
    message_id: int
    created_at: datetime
