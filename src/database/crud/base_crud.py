from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.database.sql_database_manager import SQLDatabaseManager
    from src.database.models import BaseModel

from abc import ABC, abstractmethod


class BaseCRUD(ABC):
    _manager: "SQLDatabaseManager"

    @abstractmethod
    async def create(self, model: "BaseModel") -> int:
        raise NotImplemented

    @abstractmethod
    async def read_all(self) -> List["BaseModel"]:
        raise NotImplemented
