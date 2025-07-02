from contextlib import contextmanager
from typing import (
    Iterator,
    Optional,
    Sequence,
    Tuple,
    Any,
    Dict,
    List
)

from redis import Redis

from langchain_core.runnables import RunnableConfig

from langgraph.checkpoint.base import (
    BaseCheckpointSaver,
    Checkpoint,
    CheckpointTuple,
    CheckpointMetadata,
    ChannelVersions,
    PendingWrite,
    WRITES_IDX_MAP,
    get_checkpoint_id
)

from .exceptions import RedisCheckpointException
from .constants import TTL
from .utils import (
    _make_redis_checkpoint_key,
    _make_redis_checkpoint_writes_key,
    _parse_redis_checkpoint_key,
    _parse_redis_checkpoint_data,
    _parse_redis_checkpoint_writes_key,
    _filter_keys,
    _load_writes
)


class RedisCheckpointSaver(BaseCheckpointSaver):
    connection: Redis

    def __init__(self, connection: Redis) -> None:
        super().__init__()
        self.connection = connection

    @classmethod
    @contextmanager
    def from_connection_params(
            cls,
            *,
            host: str,
            port: int,
            db: int
    ) -> Iterator["RedisCheckpointSaver"]:
        connection: Optional[Redis] = None
        try:
            connection = Redis(host=host, port=port, db=db)
            yield RedisCheckpointSaver(connection)
        except Exception as ex:
            raise RedisCheckpointException(ex)
        finally:
            if connection:
                connection.close()

    def put(
        self,
        config: RunnableConfig,
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
        new_versions: ChannelVersions,
    ) -> RunnableConfig:
        thread_id: str = config["configurable"]["thread_id"]
        checkpoint_ns: str = config["configurable"]["checkpoint_ns"]
        checkpoint_id: str = checkpoint["id"]
        parent_checkpoint_id: str = config["configurable"].get("checkpoint_id")
        key = _make_redis_checkpoint_key(thread_id, checkpoint_ns, checkpoint_id)

        type_, serialized_checkpoint = self.serde.dumps_typed(checkpoint)
        serialized_metadata = self.serde.dumps(metadata)
        data = {
            "checkpoint": serialized_checkpoint,
            "type": type_,
            "metadata": serialized_metadata,
            "parent_checkpoint_id": parent_checkpoint_id
            if parent_checkpoint_id
            else "",
        }
        self.connection.hset(key, mapping=data)
        self.connection.expire(key, TTL)
        return {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_ns": checkpoint_ns,
                "checkpoint_id": checkpoint_id,
            }
        }

    def put_writes(
        self,
        config: RunnableConfig,
        writes: Sequence[Tuple[str, Any]],
        task_id: str,
        task_path: str = "",
    ) -> None:
        thread_id: str = config["configurable"]["thread_id"]
        checkpoint_ns: str = config["configurable"]["checkpoint_ns"]
        checkpoint_id: str = config["configurable"]["checkpoint_id"]

        for idx, (channel, value) in enumerate(writes):
            key = _make_redis_checkpoint_writes_key(
                thread_id,
                checkpoint_ns,
                checkpoint_id,
                task_id,
                WRITES_IDX_MAP.get(channel, idx),
            )
            type_, serialized_value = self.serde.dumps_typed(value)
            data = {"channel": channel, "type": type_, "value": serialized_value}
            if all(w[0] in WRITES_IDX_MAP for w in writes):
                self.connection.hset(key, mapping=data)
                self.connection.expire(key, TTL)
            else:
                for field, value in data.items():
                    self.connection.hsetnx(key, field, value)
                    self.connection.expire(key, TTL)

    def get_tuple(self, config: RunnableConfig) -> Optional[CheckpointTuple]:
        thread_id: str = config["configurable"]["thread_id"]
        checkpoint_id: str = get_checkpoint_id(config)
        checkpoint_ns: str = config["configurable"].get("checkpoint_ns", "")

        checkpoint_key = self._get_checkpoint_key(
            self.connection, thread_id, checkpoint_ns, checkpoint_id
        )
        if not checkpoint_key:
            return None

        checkpoint_data = self.connection.hgetall(checkpoint_key)

        checkpoint_id = (
                checkpoint_id
                or _parse_redis_checkpoint_key(checkpoint_key)["checkpoint_id"]
        )
        pending_writes = self._load_pending_writes(
            thread_id, checkpoint_ns, checkpoint_id
        )
        return _parse_redis_checkpoint_data(
            self.serde, checkpoint_key, checkpoint_data, pending_writes=pending_writes
        )

    def list(
        self,
        config: Optional[RunnableConfig],
        *,
        filter: Optional[Dict[str, Any]] = None,
        before: Optional[RunnableConfig] = None,
        limit: Optional[int] = None,
    ) -> Iterator[CheckpointTuple]:
        thread_id = config["configurable"]["thread_id"]
        checkpoint_ns = config["configurable"].get("checkpoint_ns", "")
        pattern = _make_redis_checkpoint_key(thread_id, checkpoint_ns, "*")

        keys = _filter_keys(self.connection.keys(pattern), before, limit)
        for key in keys:
            data = self.connection.hgetall(key)
            if data and b"checkpoint" in data and b"metadata" in data:
                # load pending writes
                checkpoint_id = _parse_redis_checkpoint_key(key.decode())[
                    "checkpoint_id"
                ]
                pending_writes = self._load_pending_writes(
                    thread_id, checkpoint_ns, checkpoint_id
                )
                yield _parse_redis_checkpoint_data(
                    self.serde, key.decode(), data, pending_writes=pending_writes
                )

    def _load_pending_writes(
            self,
            thread_id: str,
            checkpoint_ns: str,
            checkpoint_id: str
    ) -> List[PendingWrite]:
        writes_key = _make_redis_checkpoint_writes_key(
            thread_id, checkpoint_ns, checkpoint_id, "*", None
        )
        matching_keys = self.connection.keys(pattern=writes_key)
        parsed_keys = [
            _parse_redis_checkpoint_writes_key(key.decode()) for key in matching_keys
        ]
        pending_writes = _load_writes(
            self.serde,
            {
                (parsed_key["task_id"], parsed_key["idx"]): self.connection.hgetall(key)
                for key, parsed_key in sorted(
                zip(matching_keys, parsed_keys), key=lambda x: x[1]["idx"]
            )
            },
        )
        return pending_writes

    @staticmethod
    def _get_checkpoint_key(
            connection: Redis,
            thread_id: str,
            checkpoint_ns: str,
            checkpoint_id: Optional[str]
    ) -> Optional[str]:
        if checkpoint_id:
            return _make_redis_checkpoint_key(thread_id, checkpoint_ns, checkpoint_id)
        all_keys = connection.keys(_make_redis_checkpoint_key(thread_id, checkpoint_ns, "*"))
        if not all_keys:
            return None

        latest_key = max(
            all_keys,
            key=lambda k: _parse_redis_checkpoint_key(k.decode())["checkpoint_id"],
        )
        return latest_key.decode()
