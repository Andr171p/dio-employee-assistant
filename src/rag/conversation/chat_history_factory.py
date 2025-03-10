from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories.redis import RedisChatMessageHistory


class ChatHistoryFactory:
    def __init__(
            self,
            redis_url: str = "redis://localhost:6379/0",
            ttl: int = 3600,
    ) -> None:
        self._redis_url = redis_url
        self._ttl = ttl

    def get_or_create_chat_history(self, session_id: str) -> BaseChatMessageHistory:
        return RedisChatMessageHistory(
            session_id=session_id,
            url=self._redis_url,
            ttl=self._ttl,
        )
