from typing import TYPE_CHECKING, List, Union

if TYPE_CHECKING:
    from src.database.database_manager import DatabaseManager
    from src.database.models import BaseModel

from abc import ABC, abstractmethod


class BaseCRUD(ABC):
    _manager: "DatabaseManager"

    @abstractmethod
    async def create(self, model: "BaseModel") -> int:
        raise NotImplemented

    @abstractmethod
    async def read_all(self) -> List["BaseModel"]:
        raise NotImplemented
