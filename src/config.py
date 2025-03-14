import os
from pathlib import Path
from typing import Literal
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / '.env'

load_dotenv(dotenv_path=ENV_PATH)


class BotSettings(BaseSettings):
    token: str = os.getenv("BOT_TOKEN")


class EmbeddingsSettings(BaseSettings):
    # model_name: str = "ai-forever/sbert_large_nlu_ru"
    model_name: str = "intfloat/multilingual-e5-large"
    model_kwargs: dict = {"device": "cpu"}
    encode_kwargs: dict = {"normalize_embeddings": False}


class CrossEncoderSettings(BaseSettings):
    model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    device: Literal["cpu", "cuda"] = "cpu"


class ChromaSettings(BaseSettings):
    collection_name: str = "dio-consult"
    persist_directory: str = os.path.join(BASE_DIR, "chroma")


class ElasticSettings(BaseSettings):
    url: str = os.getenv("ELASTIC_URL")
    user: str = os.getenv("ELASTIC_USER")
    password: str = os.getenv("ELASTIC_PASSWORD")


class PromptsSettings(BaseSettings):
    rag_prompt: str = os.path.join(BASE_DIR, "prompts", "Промпт_ДИО_сотрудник.txt")
    rag_prompt_with_chat_history: str = os.path.join(BASE_DIR, "prompts", "Промпт_ДИО_сотрудник_с_историей_сообщений.txt")


class GigaChatSettings(BaseSettings):
    api_key: str = os.getenv("GIGACHAT_API_KEY")
    scope: str = os.getenv("GIGACHAT_SCOPE")


class DatabaseSettings(BaseSettings):
    db_path: str = os.path.join(BASE_DIR, "db.sqlite3")
    driver: str = "aiosqlite"
    url: str = f"sqlite+{driver}:///{db_path}"


class Settings(BaseSettings):
    bot: BotSettings = BotSettings()
    embeddings: EmbeddingsSettings = EmbeddingsSettings()
    cross_encoder: CrossEncoderSettings = CrossEncoderSettings()
    elastic: ElasticSettings = ElasticSettings()
    chroma: ChromaSettings = ChromaSettings()
    prompts: PromptsSettings = PromptsSettings()
    giga_chat: GigaChatSettings = GigaChatSettings()
    db: DatabaseSettings = DatabaseSettings()


settings = Settings()
