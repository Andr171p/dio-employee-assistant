from datetime import datetime

from pydantic import BaseModel


class Dialog(BaseModel):
    user_message: str
    chat_bot_message: str
    message_id: int
    created_at: datetime
