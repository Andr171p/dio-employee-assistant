from pathlib import Path
from dotenv import load_dotenv

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)

POSTGRES_DRIVER = "asyncpg"


class BotSettings(BaseSettings):
    token: str = ""

    model_config = SettingsConfigDict(env_prefix="BOT_")


class EmbeddingsSettings(BaseModel):
    model_name: str = "deepvk/USER-bge-m3"
    model_kwargs: dict = {"device": "cpu"}
    encode_kwargs: dict = {"normalize_embeddings": False}


class ElasticSettings(BaseSettings):
    host: str = "elastic"
    port: int = 9200
    username: str = "user"
    password: str = "password"

    model_config = SettingsConfigDict(env_prefix="ELASTIC_")

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"

    @property
    def auth(self) -> tuple[str, str]:
        return self.username, self.password


class RedisSettings(BaseSettings):
    host: str = "redis"
    port: int = 6379

    model_config = SettingsConfigDict(env_prefix="REDIS_")

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/0"


class GigaChatSettings(BaseSettings):
    api_key: str = ""
    scope: str = ""
    model_name: str = ""

    model_config = SettingsConfigDict(env_prefix="GIGACHAT_")


class YandexCloudSettings(BaseSettings):
    folder_id: str = ""
    api_key: str = ""

    model_config = SettingsConfigDict(env_prefix="YANDEX_")


class PostgresSettings(BaseSettings):
    host: str = "postgres"
    port: int = 5432
    user: str = "postgres"
    password: str = "postgres"
    db: str = "postgres"

    model_config = SettingsConfigDict(env_prefix="POSTGRES_")

    @property
    def url(self) -> str:
        return f"postgresql+{POSTGRES_DRIVER}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class Settings(BaseSettings):
    bot: BotSettings = BotSettings()
    embeddings: EmbeddingsSettings = EmbeddingsSettings()
    elastic: ElasticSettings = ElasticSettings()
    redis: RedisSettings = RedisSettings()
    gigachat: GigaChatSettings = GigaChatSettings()
    yandexcloud: YandexCloudSettings = YandexCloudSettings()
    postgres: PostgresSettings = PostgresSettings()
