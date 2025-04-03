from dishka import Provider, provide, Scope

from langchain_gigachat import GigaChat
from langchain_core.embeddings import Embeddings
from langchain_community.llms.yandex import YandexGPT
# from langchain_core.language_models import BaseChatModel, LLM

from src.ai_agent import DIOAgent
from src.ai_agent.nodes import LibrarianNode, RAGNode


class AgentProvider(Provider):
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
    def get_agent(
            self,
            librarian_node: LibrarianNode,
            rag_node: RAGNode
    ) -> DIOAgent:
        return DIOAgent(librarian_node, rag_node)
