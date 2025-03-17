from abc import ABC, abstractmethod


class BaseAgent(ABC):
    @abstractmethod
    async def generate(self, question: str) -> str:
        raise NotImplementedError
