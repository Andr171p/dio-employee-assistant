from aiogram import F, Router
from aiogram.types import Message
from dishka.integrations.aiogram import FromDishka

from src.presentation.bot.controllers import ChatBotController


chatbot_router = Router()


@chatbot_router.message(F.text)
async def answer(message: Message, chatbot_controller: FromDishka[ChatBotController]) -> None:
    await chatbot_controller.answer_on_message(message)
