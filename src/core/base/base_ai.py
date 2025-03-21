from typing import Union

from abc import ABC, abstractmethod


class BaseAI(ABC):
    @abstractmethod
    async def generate(self, query: str) -> Union[dict, str]:
        raise NotImplementedError
