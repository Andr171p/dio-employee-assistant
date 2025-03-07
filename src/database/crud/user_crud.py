from typing import TYPE_CHECKING, Union, Sequence

if TYPE_CHECKING:
    from src.database.database_manager import DatabaseManager

from sqlalchemy import select, func

from src.database.crud.base_crud import BaseCRUD
from src.database.models import UserModel


class UserCRUD(BaseCRUD):
    def __init__(self, manager: "DatabaseManager") -> None:
        self._manager = manager

    async def create(self, user: UserModel) -> None:
        async with self._manager.session() as session:
            session.add(user)
            id = user.id
            await session.commit()
        return id

    async def read_by_user_id(self, user_id: int) -> Union[UserModel, None]:
        async with self._manager.session() as session:
            stmt = (
                select(UserModel)
                .where(UserModel.user_id == user_id)
            )
            user = await session.execute(stmt)
        return user.scalar_one_or_none()

    async def read_all(self) -> Union[Sequence[UserModel], None]:
        async with self._manager.session() as session:
            stmt = select(UserModel)
            user = await session.execute(stmt)
        return user.scalars().all()

    async def read_total_count(self) -> Union[int, None]:
        async with self._manager.session() as session:
            stmt = (
                select(func.count)
                .select_from(UserModel)
            )
            count = await session.execute(stmt)
        return count.scalar_one_or_none()
