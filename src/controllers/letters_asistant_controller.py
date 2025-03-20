from aiogram.types import Message

from src.presenters import AILetterPresenter
from src.services.file_loader import TelegramFileLoader
from src.core.use_cases import LettersAssistantUseCase


class LettersAssistantController:
    def __init__(
            self,
            letters_assistant_use_case: LettersAssistantUseCase,
            telegram_file_loader: TelegramFileLoader
    ) -> None:
        self._letters_assistant_use_case = letters_assistant_use_case
        self._telegram_file_loader = telegram_file_loader

    async def assist(self, message: Message) -> None:
        await message.bot.send_chat_action(message.chat.id, action="typing")
        letters_file = await self._telegram_file_loader.load(message)
        ai_letter = await self._letters_assistant_use_case.assist(letters_file)
        await AILetterPresenter(message).present(ai_letter)
