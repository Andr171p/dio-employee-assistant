from typing import List, Dict
from abc import ABC, abstractmethod


class BaseChatMemory(ABC):
    @abstractmethod
    def get_messages(self) -> List[Dict]:
        raise NotImplementedError

    @abstractmethod
    def add_message(self, message: Dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError