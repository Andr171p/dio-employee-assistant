from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dishka.integrations.aiogram import setup_dishka

from src.presentation.bot.routers import start_router, chatbot_router
from src.di import container


def create_dp() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        start_router,
        chatbot_router
    )
    setup_dishka(
        container=container,
        router=dp,
        auto_inject=True
    )
    return dp
