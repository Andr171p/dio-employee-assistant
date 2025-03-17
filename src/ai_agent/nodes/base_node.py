from abc import ABC, abstractmethod

from typing_extensions import TypedDict


class BaseNode(ABC):
    @abstractmethod
    async def execute(self, state: TypedDict) -> dict:
        raise NotImplementedError

    async def __call__(self, state: TypedDict) -> dict:
        return await self.execute(state)
