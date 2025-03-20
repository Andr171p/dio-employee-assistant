from typing import TYPE_CHECKING, BinaryIO

if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.types import Message

from src.services.file_loader.base_file_loader import BaseFileLoader


class TelegramFileLoader(BaseFileLoader):
    def __init__(self, bot: "Bot") -> None:
        self._bot = bot

    async def load(
            self,
            message: "Message",
            directory: str
    ) -> BinaryIO:
        file_id: str = message.document.file_id
        file = await self._bot.get_file(file_id)
        file_path = file.file_path
        downloaded_file = await self._bot.download_file(file_path)
        return downloaded_file
