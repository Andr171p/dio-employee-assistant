from aiogram.types import Message


class ChatBotPresenter:
    def __init__(self, message: Message) -> None:
        self._message = message

    async def present(self, chatbot_answer: str) -> int:
        message = await self._message.answer(chatbot_answer)
        return message.message_id