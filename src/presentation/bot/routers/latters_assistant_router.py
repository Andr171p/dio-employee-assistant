from aiogram import Router
from aiogram.types import Message
from dishka.integrations.aiogram import FromDishka


letters_assistant_router = Router()


@letters_assistant_router.message(content_types=["document"])
async def assist(message: Message) -> None:
    ...
