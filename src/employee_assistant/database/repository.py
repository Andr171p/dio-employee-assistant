from typing import Optional

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .models import MessageOrm

from ..schemas import BaseMessage
from ..base import MessageRepository


class SQLMessageRepository(MessageRepository):
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        self.sessionmaker = sessionmaker

    async def bulk_create(self, messages: list[BaseMessage]) -> None:
        message_orms = [MessageOrm(**message.model_dump()) for message in messages]
        async with self.sessionmaker() as session:
            session.add_all(message_orms)
            await session.commit()

    async def update(self, id: int, **kwargs) -> Optional[BaseMessage]:
        async with self.sessionmaker() as session:
            stmt = (
                update(MessageOrm)
                .where(MessageOrm.id == id)
                .values(**kwargs)
            )
            result = await session.execute(stmt)
            await session.commit()
            message = result.scalar_one_or_none()
        return BaseMessage.model_validate(message) if message else None
