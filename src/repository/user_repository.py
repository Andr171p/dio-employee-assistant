from typing import TYPE_CHECKING, List, Union

if TYPE_CHECKING:
    from src.database.crud import UserCRUD

from src.repository.base_repository import BaseRepository
from src.database.models import UserModel
from src.core.entities import User


class UserRepository(BaseRepository):
    def __init__(self, crud: "UserCRUD") -> None:
        self._crud = crud

    async def save(self, user: User) -> int | None:
        return await self._crud.create(UserModel(**user.model_dump()))

    async def get_all(self) -> List[Union[User, None]]:
        users = await self._crud.read_all()
        return [User.model_validate(user) for user in users] if users else []

    async def get_by_user_id(self, user_id: int) -> Union[User, None]:
        user = await self._crud.read_by_user_id(user_id)
        return User.model_validate(user) if user else None
