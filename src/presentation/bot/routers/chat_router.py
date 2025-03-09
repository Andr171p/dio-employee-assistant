from aiogram import F, Router
from aiogram.types import Message

from dishka.integrations.aiogram import FromDishka

from src.core.use_cases import ChatBotUseCase
from src.presentation.bot.presenters import ChatBotAnswerPresenter


chat_router = Router()


@chat_router.message(F.text)
async def answer(message: Message, chat_bot: FromDishka[ChatBotUseCase]) -> None:
    await message.bot.send_chat_action(message.chat.id, "typing")
    user_question: str = message.text
    chat_bot_answer = await chat_bot.answer(user_question)
    await ChatBotAnswerPresenter.present(message, answer=chat_bot_answer)
