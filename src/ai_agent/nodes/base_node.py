from abc import ABC, abstractmethod

from src.ai_agent.state import State


class BaseNode(ABC):
    @abstractmethod
    async def execute(self, state: State) -> dict:
        raise NotImplemented

    async def __call__(self, state: State) -> dict:
        return await self.execute(state)
