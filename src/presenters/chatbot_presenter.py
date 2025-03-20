from aiogram.types import Message


class ChatBotPresenter:
    def __init__(self, message: Message) -> None:
        self.message = message

    async def present(self, chatbot_answer: str) -> int:
        message = await self.message.answer(chatbot_answer, parse_mode="Markdown")
        return message.message_id
