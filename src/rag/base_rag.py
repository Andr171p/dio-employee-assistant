from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.runnables import Runnable

from abc import ABC, abstractmethod


class BaseRag(ABC):
    _chain: "Runnable"

    @abstractmethod
    async def generate(self, query: str) -> str:
        raise NotImplementedError
