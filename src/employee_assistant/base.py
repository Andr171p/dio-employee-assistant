from typing import Optional

from abc import ABC, abstractmethod

from .schemas import BaseMessage


class AIAgent(ABC):
    @abstractmethod
    async def generate(self, thread_id: str | int, content: str) -> str: pass


class MessageRepository(ABC):
    @abstractmethod
    async def bulk_create(self, messages: list[BaseMessage]) -> None: pass

    @abstractmethod
    async def update(self, id: int, **kwargs) -> Optional[BaseMessage]: pass
