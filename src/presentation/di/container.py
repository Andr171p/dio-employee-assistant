from dishka import make_async_container

from src.presentation.di.providers import (
    BotProvider,
    UsersProvider,
    AgentProvider,
    ChatBotProvider,
    DatabaseProvider,
    LangchainProvider,
    LettersAssistantProvider
)


container = make_async_container(
    BotProvider(),
    UsersProvider(),
    AgentProvider(),
    ChatBotProvider(),
    DatabaseProvider(),
    LangchainProvider(),
    LettersAssistantProvider()
)
