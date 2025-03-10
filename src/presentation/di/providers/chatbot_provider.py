from dishka import Provider, provide, Scope

from src.rag import BaseRAG
from src.core.use_cases import ChatBotUseCase


class ChatBotProvider(Provider):
    @provide(scope=Scope.APP)
    def get_chatbot(self, rag: BaseRAG) -> ChatBotUseCase:
        return ChatBotUseCase(rag)
