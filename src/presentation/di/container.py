from dishka import make_async_container

from src.presentation.di.providers import (
    UsersProvider,
    ChatBotProvider,
    DatabaseProvider,
    LangchainProvider,
    LettersAssistantProvider
)


container = make_async_container(
    UsersProvider(),
    ChatBotProvider(),
    DatabaseProvider(),
    LangchainProvider(),
    LettersAssistantProvider()
)
