from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from dishka.integrations.aiogram import FromDishka

from src.core.use_cases import UserUseCase
from src.mappers import UserMapper


start_router = Router()


@start_router.message(Command("start"))
async def start(message: Message, users: FromDishka[UserUseCase]) -> None:
    user = UserMapper.from_message(message)
    await users.register(user)
    await message.answer("Hello")
