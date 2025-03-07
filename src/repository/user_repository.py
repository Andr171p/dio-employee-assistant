from typing import TYPE_CHECKING, List, Union

if TYPE_CHECKING:
    from src.database.crud import UserCRUD

from src.repository.base_repository import BaseRepository
from src.database.models import UserModel
from src.core.entities import User


class UserRepository(BaseRepository):
    def __init__(self, crud: "UserCRUD") -> None:
        self._crud = crud

    async def add(self, user: User) -> int | None:
        return await self._crud.create(UserModel(**user.model_dump()))
