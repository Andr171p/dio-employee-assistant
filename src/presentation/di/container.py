from dishka import make_async_container

from src.presentation.di.providers import RAGProvider, ChatBotProvider


container = make_async_container(
    RAGProvider(),
    ChatBotProvider()
)
