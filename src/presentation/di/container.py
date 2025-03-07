from dishka import make_async_container

from src.presentation.di.providers import (
    DatabaseProvider,
    RAGProvider,
    ChatBotProvider,
    UsersProvider
)


container = make_async_container(
    DatabaseProvider(),
    RAGProvider(),
    ChatBotProvider(),
    UsersProvider()
)
