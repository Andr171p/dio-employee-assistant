from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    username: Optional[str]
    created_at: datetime
