from abc import ABC, abstractmethod

from src.ai_agent.states import ReasoningState


class BaseNode(ABC):
    @abstractmethod
    async def execute(self, state: ReasoningState) -> dict:
        raise NotImplementedError

    async def __call__(self, state: ReasoningState) -> dict:
        return await self.execute(state)
