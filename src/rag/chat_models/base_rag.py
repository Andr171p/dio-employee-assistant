from abc import ABC, abstractmethod


class BaseRAG(ABC):
    @abstractmethod
    async def generate(self, query: str, **kwargs) -> str:
        raise NotImplementedError
