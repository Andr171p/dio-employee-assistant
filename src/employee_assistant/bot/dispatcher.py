from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from dishka.integrations.aiogram import setup_dishka

from .handlers import router

from ..container import container


def create_dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    setup_dishka(container=container, router=dp, auto_inject=True)
    return dp
