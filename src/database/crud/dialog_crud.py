from typing import TYPE_CHECKING, List

from sqlalchemy import select

if TYPE_CHECKING:
    from src.database.sql_database_manager import SQLDatabaseManager

from src.database.crud.base_crud import BaseCRUD
from src.database.models import DialogModel


class DialogCRUD(BaseCRUD):
    def __init__(self, manager: "SQLDatabaseManager") -> None:
        self._manager = manager

    async def create(self, dialog: DialogModel) -> int:
        async with self._manager.session() as session:
            session.add(dialog)
            id = dialog.id
            await session.commit()
        return id

    async def read_by_user_id(self, user_id: int) -> List[DialogModel]:
        async with self._manager.session() as session:
            stmt = (
                select(DialogModel)
                .where(DialogModel.user_id == user_id)
            )
            dialogs = await session.execute(stmt)
        return dialogs.scalars().all()

    async def read_all(self) -> List[DialogModel]:
        async with self._manager.session() as session:
            stmt = select(DialogModel)
            dialogs = await session.execute(stmt)
        return dialogs.scalars().all()
