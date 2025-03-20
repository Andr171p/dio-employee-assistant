from abc import ABC, abstractmethod


class BaseAgent(ABC):
    @abstractmethod
    async def generate(self, query: str) -> dict:
        raise NotImplementedError
