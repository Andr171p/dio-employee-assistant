from typing import Optional

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from .models import MessageOrm

from ..schemas import BaseMessage


async def insert_messages(session: AsyncSession, messages: list[BaseMessage]) -> None:
    message_orms = [MessageOrm(**message.model_dump()) for message in messages]
    session.add_all(message_orms)
    await session.commit()


async def update_message(session: AsyncSession, id: int, **kwargs) -> Optional[BaseMessage]:
    stmt = (
        update(MessageOrm)
        .values(**kwargs)
        .where(MessageOrm.id == id)
        .returning(MessageOrm)
    )
    result = await session.execute(stmt)
    await session.commit()
    message = result.scalar_one_or_none()
    return BaseMessage.model_validate(message) if message else None
