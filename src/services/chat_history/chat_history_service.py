from typing import Union, List, Dict

import json
import redis


class ChatHistoryService:
    def __init__(self, redis_client: redis.Redis) -> None:
        self.redis_client = redis_client

    def save_messages(
            self,
            user_id: Union[int, str],
            messages: List[Dict[str, str]],
            ttl: int = 3600
    ) -> None:
        self.redis_client.set(user_id, json.dumps(messages), ex=ttl)

    def get_messages(self, user_id: Union[int, str]) -> List[Dict[str, str]]:
        messages = self.redis_client.get(user_id)
        return json.loads(messages) if messages else []
