from dishka import Provider, provide, Scope

from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel, LLM

from src.dio_ai.agent import Agent
from src.dio_ai.nodes import LibrarianNode, RAGNode


class AgentProvider(Provider):
    @provide(scope=Scope.APP)
    def get_librarian_node(self, model: BaseChatModel | LLM) -> LibrarianNode:
        return LibrarianNode(model)

    @provide(scope=Scope.APP)
    def get_rag_node(
            self,
            embeddings: Embeddings,
            model: BaseChatModel | LLM
    ) -> RAGNode:
        return RAGNode(embeddings, model)

    @provide(scope=Scope.APP)
    def get_agent(
            self,
            librarian_node: LibrarianNode,
            rag_node: RAGNode
    ) -> Agent:
        return Agent(librarian_node, rag_node)
