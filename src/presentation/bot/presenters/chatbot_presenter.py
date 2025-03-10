from aiogram.types import Message
from pydantic import BaseModel


class ChatBotPresenter(BaseModel):
    message: Message

    async def present(self, answer: str) -> int:
        message = await self.message.answer(answer)
        return message.message_id