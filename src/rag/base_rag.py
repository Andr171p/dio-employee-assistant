from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.runnables import Runnable

from abc import ABC, abstractmethod


class BaseRAG(ABC):
    @abstractmethod
    def _get_chain(self) -> "Runnable":
        """Method must be implemented RAG chain factory."""
        raise NotImplementedError

    @abstractmethod
    async def generate(self, query: str, **kwargs) -> str:
        """Method must be implemented to generate the response."""
        raise NotImplementedError
