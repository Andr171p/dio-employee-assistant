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
from langchain_core.prompts import ChatPromptTemplate
from langchain_gigachat import GigaChat
from langchain_core.output_parsers.string import StrOutputParser

from src.rag import BaseRAG
from src.rag.naive import NaiveRAG
from src.misc.file_readers import read_txt
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
    def get_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_template(read_txt(settings.prompts.prompt_path))

    @provide(scope=Scope.APP)
    def get_model(self) -> BaseChatModel:
        return GigaChat(
            credentials=settings.giga_chat.api_key,
            scope=settings.giga_chat.scope,
            verify_ssl_certs=False,
            profanity_check=False
        )

    @provide(scope=Scope.APP)
    def get_parser(self) -> StrOutputParser:
        return StrOutputParser()

    @provide(scope=Scope.APP)
    def get_rag(
            self,
            retriever: BaseRetriever,
            prompt: ChatPromptTemplate,
            model: BaseChatModel,
            parser: StrOutputParser
    ) -> BaseRAG:
        return NaiveRAG(
            retriever=retriever,
            prompt=prompt,
            model=model,
            parser=parser
        )
