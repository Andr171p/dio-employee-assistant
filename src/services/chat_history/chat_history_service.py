from typing import Union, List, Dict

import json
import redis
import hashlib


class ChatHistoryService:
    def __init__(self, redis_client: redis.Redis) -> None:
        self.redis_client = redis_client

    @staticmethod
    def _get_key(user_id: Union[int, str]) -> str:
        hashed_user_id: str = hashlib.sha256(user_id.encode()).hexdigest()
        return hashed_user_id

    def save_messages(
            self,
            user_id: Union[int, str],
            messages: List[Dict[str, str]],
            ttl: int = 3600
    ) -> None:
        key = self._get_key(user_id)
        self.redis_client.set(key, json.dumps(messages), ex=ttl)

    def get_messages(self, user_id: Union[int, str]) -> List[Union[Dict[str, str], None]]:
        key = self._get_key(user_id)
        messages = self.redis_client.get(key)
        return json.loads(messages) if messages else []
