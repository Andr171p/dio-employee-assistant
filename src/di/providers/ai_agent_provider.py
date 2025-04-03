from dishka import Provider, provide, Scope

from langchain_gigachat import GigaChat
from langchain_core.embeddings import Embeddings
from langchain_community.llms.yandex import YandexGPT
# from langchain_core.language_models import BaseChatModel, LLM

from src.ai_agent import DIOAIAgent
from src.core.base import BaseAIAssistant
from src.ai_agent.nodes import LibrarianNode, RAGNode


class AIAgentProvider(Provider):
    @provide(scope=Scope.APP)
    def get_librarian_node(self, model: GigaChat) -> LibrarianNode:
        return LibrarianNode(model)

    @provide(scope=Scope.APP)
    def get_rag_node(
            self,
            embeddings: Embeddings,
            model: YandexGPT
    ) -> RAGNode:
        return RAGNode(embeddings, model)

    @provide(scope=Scope.APP)
    def get_ai_agent(
            self,
            librarian_node: LibrarianNode,
            rag_node: RAGNode
    ) -> BaseAIAssistant:
        return DIOAIAgent(librarian_node, rag_node)
