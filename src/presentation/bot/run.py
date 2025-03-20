from aiogram import Bot

from src.presentation.di import container
from src.presentation.bot.dp import create_dp


async def run_bot() -> None:
    bot = container.get(Bot)
    dp = create_dp()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
