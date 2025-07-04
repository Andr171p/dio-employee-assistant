import os
from pathlib import Path
from dotenv import load_dotenv

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV_PATH = BASE_DIR / ".env"

PG_DRIVER = "asyncpg"

load_dotenv(dotenv_path=ENV_PATH)


class BotSettings(BaseSettings):
    TOKEN: str = os.getenv("BOT_TOKEN")


class EmbeddingsSettings(BaseSettings):
    MODEL_NAME: str = "deepvk/USER-bge-m3"
    MODEL_KWARGS: dict = {"device": "cpu"}
    ENCODE_KWARGS: dict = {"normalize_embeddings": False}


class ElasticSettings(BaseSettings):
    ELASTIC_HOST: str = os.getenv("ELASTIC_HOST")
    ELASTIC_PORT: int = os.getenv("ELASTIC_PORT")
    ELASTIC_USER: str = os.getenv("ELASTIC_USER")
    ELASTIC_PASSWORD: str = os.getenv("ELASTIC_PASSWORD")

    @property
    def elastic_url(self) -> str:
        return f"http://{self.ELASTIC_HOST}:{self.ELASTIC_PORT}"


class RedisSettings(BaseSettings):
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = os.getenv("REDIS_PORT")

    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"


class GigaChatSettings(BaseSettings):
    API_KEY: str = os.getenv("GIGACHAT_API_KEY")
    SCOPE: str = os.getenv("GIGACHAT_SCOPE")
    MODEL_NAME: str = os.getenv("GIGACHAT_MODEL_NAME")


class YandexGPTSettings(BaseSettings):
    FOLDER_ID: str = os.getenv("YANDEX_FOLDER_ID")
    API_KEY: str = os.getenv("YANDEX_GPT_API_KEY")


class PostgresSettings(BaseSettings):
    PG_HOST: str = os.getenv("POSTGRES_HOST")
    PG_PORT: int = os.getenv("POSTGRES_PORT")
    PG_USER: str = os.getenv("POSTGRES_USER")
    PG_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    PG_DB: str = os.getenv("POSTGRES_DB")

    @property
    def sqlalchemy_url(self) -> str:
        return f"postgresql+{PG_DRIVER}://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"


class Settings(BaseSettings):
    bot: BotSettings = BotSettings()
    embeddings: EmbeddingsSettings = EmbeddingsSettings()
    elasticsearch: ElasticSettings = ElasticSettings()
    giga_chat: GigaChatSettings = GigaChatSettings()
    yandex_gpt: YandexGPTSettings = YandexGPTSettings()
    postgres: PostgresSettings = PostgresSettings()
