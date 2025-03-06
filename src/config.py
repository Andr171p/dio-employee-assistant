import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / '.env'

load_dotenv(dotenv_path=ENV_PATH)


class BotSettings(BaseSettings):
    token: str = os.getenv("BOT_TOKEN")


class EmbeddingsSettings(BaseSettings):
    model_name: str = "ai-forever/sbert_large_nlu_ru"
    model_kwargs: dict = {"device": "cpu"}
    encode_kwargs: dict = {"normalize_embeddings": False}


class ChromaSettings(BaseSettings):
    collection_name: str = "dio-consult"
    persist_directory: str = os.path.join(BASE_DIR, "chroma")


class PromptsSettings(BaseSettings):
    prompt_path: str = os.path.join(BASE_DIR, "prompts", "Промпт_ДИО_сотрудник.txt")


class GigaChatSettings(BaseSettings):
    api_key: str = os.getenv("GIGACHAT_API_KEY")
    scope: str = os.getenv("GIGACHAT_SCOPE")


class Settings(BaseSettings):
    bot: BotSettings = BotSettings()
    embeddings: EmbeddingsSettings = EmbeddingsSettings()
    chroma: ChromaSettings = ChromaSettings()
    prompts: PromptsSettings = PromptsSettings()
    giga_chat: GigaChatSettings = GigaChatSettings()


settings = Settings()
