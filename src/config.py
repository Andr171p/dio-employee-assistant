import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / '.env'

load_dotenv(dotenv_path=ENV_PATH)


class BotSettings(BaseSettings):
    token: str = os.getenv("BOT_TOKEN")


class ChromaSettings(BaseSettings):
    collection_name: str = "dio-consult"
    persist_directory: str = os.path.join(BASE_DIR, os.getenv("chroma"))


class Settings(BaseSettings):
    bot: BotSettings = BotSettings()
    chroma: ChromaSettings = ChromaSettings()


settings = Settings()
