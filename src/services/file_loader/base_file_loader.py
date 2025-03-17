from typing import Any

from abc import ABC, abstractmethod


class BaseFileLoader(ABC):
    @abstractmethod
    async def load(self, *args) -> Any:
        raise NotImplementedError
