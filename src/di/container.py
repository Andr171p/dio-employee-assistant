from dishka import make_async_container

from src.di.providers import (
    BotProvider,
    UsersProvider,
    AIAgentProvider,
    ChatBotProvider,
    DatabaseProvider,
    LangchainProvider
)


container = make_async_container(
    BotProvider(),
    UsersProvider(),
    AIAgentProvider(),
    ChatBotProvider(),
    DatabaseProvider(),
    LangchainProvider()
)
