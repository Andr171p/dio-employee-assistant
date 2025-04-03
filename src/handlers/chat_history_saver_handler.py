from typing import Callable, Coroutine, Any, TypeVar
from datetime import datetime
from functools import wraps

from src.core.entities import Dialog


T = TypeVar("T", bound="ChatBotUseCase")


def chat_history_saver(
        func: Callable[[T, str, Any], Coroutine[Any, Any, str]]
) -> Callable[[T, str, Any], Coroutine[Any, Any, str]]:
    @wraps(func)
    async def wrapper(self: T, question: str, *args, **kwargs) -> str:
        user_id = kwargs.get("user_id")
        if user_id is None:
            raise ValueError("user_id is required")
        answer = await func(self, question, *args, **kwargs)
        if self._dialog_repository:
            dialog = Dialog(
                user_id=user_id,
                user_message=question,
                chatbot_message=answer,
                created_at=datetime.now()
            )
            await self._dialog_repository.save(dialog)
        return answer
    return wrapper
