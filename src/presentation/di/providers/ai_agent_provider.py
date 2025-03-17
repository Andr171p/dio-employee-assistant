from dishka import Provider, provide, Scope

from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever
from langchain_core.retrievers import BaseRetriever
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.embeddings import HuggingFaceEmbeddings
from elasticsearch import Elasticsearch
from langchain_community.retrievers import ElasticSearchBM25Retriever
from langchain.retrievers import EnsembleRetriever
import chromadb
from langchain_chroma import Chroma
from langchain_gigachat import GigaChat

from src.ai_agents import AIAgent, BaseAIAgent
from src.ai_agents.nodes import (
    DecisionNode,
    RewriterNode,
    RetrieverNode,
    GenerationNode
)
from src.config import settings


class RAGProvider(Provider):
    @provide(scope=Scope.APP)
    def get_embeddings(self) -> Embeddings:
        return HuggingFaceEmbeddings(
            model_name=settings.embeddings.model_name,
            model_kwargs=settings.embeddings.model_kwargs,
            encode_kwargs=settings.embeddings.encode_kwargs,
        )

    @provide(scope=Scope.APP)
    def get_vector_store(self, embeddings: Embeddings) -> VectorStore:
        return Chroma(
            client=chromadb.PersistentClient(settings.chroma.persist_directory),
            collection_name=settings.chroma.collection_name,
            embedding_function=embeddings
        )

    @provide(scope=Scope.APP)
    def get_elastic(self) -> Elasticsearch:
        return Elasticsearch(
            hosts=settings.elastic.url,
            basic_auth=(settings.elastic.user, settings.elastic.password),
            verify_certs=False
        )

    @provide(scope=Scope.APP)
    def get_bm25_retriever(self, elastic: Elasticsearch) -> ElasticSearchBM25Retriever:
        return ElasticSearchBM25Retriever(
            client=elastic,
            index_name="dio-consult"
        )

    @provide(scope=Scope.APP)
    def get_vector_store_retriever(self, vector_store: VectorStore) -> VectorStoreRetriever:
        return vector_store.as_retriever()

    @provide(scope=Scope.APP)
    def get_retriever(
            self,
            vector_store_retriever: VectorStoreRetriever,
            bm25_retriever: ElasticSearchBM25Retriever
    ) -> BaseRetriever:
        return EnsembleRetriever(
            retrievers=[vector_store_retriever, bm25_retriever],
            weights=[0.6, 0.4]
        )

    @provide(scope=Scope.APP)
    def get_model(self) -> BaseChatModel:
        return GigaChat(
            credentials=settings.giga_chat.api_key,
            scope=settings.giga_chat.scope,
            verify_ssl_certs=False,
            profanity_check=False
        )

    @provide(scope=Scope.APP)
    def get_decision_node(self, model: BaseChatModel) -> DecisionNode:
        return DecisionNode(model)

    @provide(scope=Scope.APP)
    def get_rewriter_node(self, model: BaseChatModel) -> RewriterNode:
        return RewriterNode(model)

    @provide(scope=Scope.APP)
    def get_retriever_node(self, retriever: BaseRetriever) -> RetrieverNode:
        return RetrieverNode(retriever)

    @provide(scope=Scope.APP)
    def get_generation_node(self, model: BaseChatModel) -> GenerationNode:
        return GenerationNode(model)

    @provide(scope=Scope.APP)
    def get_ai_agent(
            self,
            decision: DecisionNode,
            rewriter: RewriterNode,
            retriever: RetrieverNode,
            generation: GenerationNode
    ) -> BaseAIAgent:
        return AIAgent(
            decision=decision,
            rewriter=rewriter,
            retriever=retriever,
            generation=generation
        )
