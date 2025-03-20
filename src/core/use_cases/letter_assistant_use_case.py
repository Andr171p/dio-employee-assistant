from src.services.file_loader import BaseFileLoader


class LetterAssistantUseCase:
    def __init__(self, file_loader: BaseFileLoader) -> None:
        self._file_loader = file_loader

    async def assist(self) -> ...:
        ...
