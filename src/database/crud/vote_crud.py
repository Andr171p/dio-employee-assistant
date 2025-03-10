from typing import TYPE_CHECKING, Union, Sequence

if TYPE_CHECKING:
    from src.database.sql_database_manager import SQLDatabaseManager

from sqlalchemy import select

from src.database.crud.base_crud import BaseCRUD
from src.database.models import VoteModel


class VoteCRUD(BaseCRUD):
    def __init__(self, manager: "SQLDatabaseManager") -> None:
        self._manager = manager

    async def create(self, vote: VoteModel) -> int:
        async with self._manager.session() as session:
            session.add(vote)
            id = vote.id
            await session.commit()
        return id

    async def read_by_message_id(self, message_id: int) -> Union[VoteModel, None]:
        async with self._manager.session() as session:
            stmt = (
                select(VoteModel)
                .where(VoteModel.message_id == message_id)
            )
            vote = await session.execute(stmt)
        return vote.scalar_one_or_none()

    async def read_all(self) -> Sequence[VoteModel]:
        async with self._manager.session() as session:
            stmt = select(VoteModel)
            votes = await session.execute(stmt)
        return votes.scalars().all()
