from typing import Optional

from abc import ABC, abstractmethod
from pathlib import Path

from .schemas import BaseMessage, MarkdownDocument


class AIAgent(ABC):
    @abstractmethod
    async def generate(self, thread_id: str | int, content: str) -> str: pass


class MessageRepository(ABC):
    @abstractmethod
    async def bulk_create(self, messages: list[BaseMessage]) -> None: pass

    @abstractmethod
    async def update(self, id: int, **kwargs) -> Optional[BaseMessage]: pass


class LoadFileError(Exception):
    pass


class Document2MarkdownLoader(ABC):
    @abstractmethod
    def load(self, file_path: Path | str, **kwargs) -> MarkdownDocument: pass
