from abc import ABC, abstractmethod

from aiogram.types import Message


class BasePresenter(ABC):
    @classmethod
    @abstractmethod
    async def present(cls, message: Message, **kwargs) -> None:
        raise NotImplemented
