from typing import Union

from abc import ABC, abstractmethod


class BaseAIAssistant(ABC):
    @abstractmethod
    async def generate(self, user_question: str) -> Union[dict, str]:
        raise NotImplementedError
