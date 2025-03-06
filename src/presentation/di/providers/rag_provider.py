from threading import settrace

from dishka import Provider, provide, Scope

from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from langchain_core.retrievers import BaseRetriever
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.embeddings import HuggingFaceEmbeddings
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
    def get_retriever(self, vector_store: VectorStore) -> BaseRetriever:
        return vector_store.as_retriever()

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
