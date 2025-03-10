from typing import Callable, Coroutine, Any
from functools import wraps

from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import RedisChatMessageHistory


def chat_history_saver(redis_url: str):
    def decorator(func: Callable[..., Coroutine[Any, Any, str]]):
        @wraps(func)
        async def wrapper(self, query: str, session_id: str, **kwargs) -> str:
            chat_history = RedisChatMessageHistory(
                url=redis_url,
                session_id=session_id,
            )
            chat_history.add_message(HumanMessage(content=query))
            response = await func(self, query, **kwargs)
            chat_history.add_message(AIMessage(content=response))
            return response
        return wrapper
    return decorator