from aiogram.types import Message

from src.core.use_cases import ChatBotUseCase
from src.presenters import ChatBotPresenter


class ChatBotController:
    def __init__(self, chatbot_use_case: ChatBotUseCase) -> None:
        self._chatbot_use_case = chatbot_use_case

    async def answer(self, message: Message) -> None:
        await message.bot.send_chat_action(message.chat.id, action="typing")
        user_id = message.from_user.id
        user_question = message.text
        chatbot_answer = await self._chatbot_use_case.answer(user_question, user_id=user_id)
        await ChatBotPresenter(message).present(chatbot_answer)
