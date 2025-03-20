from aiogram import F, Router
from aiogram.types import Message
from dishka.integrations.aiogram import FromDishka

from src.controllers import LettersAssistantController


letters_assistant_router = Router()


@letters_assistant_router.message(F.document)
async def assist(
        message: Message,
        letters_assistant_controller: FromDishka[LettersAssistantController]
) -> None:
    await letters_assistant_controller.assist(message)
