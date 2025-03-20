from dishka import make_async_container

from src.presentation.di.providers import (
    BotProvider,
    UsersProvider,
    ChatBotProvider,
    DatabaseProvider,
    LangchainProvider,
    LettersAssistantProvider
)


container = make_async_container(
    BotProvider(),
    UsersProvider(),
    ChatBotProvider(),
    DatabaseProvider(),
    LangchainProvider(),
    LettersAssistantProvider()
)
