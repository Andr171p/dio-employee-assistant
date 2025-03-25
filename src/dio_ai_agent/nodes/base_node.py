from abc import ABC, abstractmethod

from src.dio_ai_agent.state import GraphState


class BaseNode(ABC):
    @abstractmethod
    async def execute(self, state: GraphState) -> dict:
        raise NotImplemented

    async def __call__(self, state: GraphState) -> dict:
        return await self.execute(state)
