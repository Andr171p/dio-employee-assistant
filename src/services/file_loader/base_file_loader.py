from typing import BinaryIO

from abc import ABC, abstractmethod


class BaseFileLoader(ABC):
    @abstractmethod
    async def load(self, *args) -> BinaryIO:
        raise NotImplementedError
