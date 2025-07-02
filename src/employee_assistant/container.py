from dishka import Provider, provide, Scope, from_context, make_async_container

from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from elasticsearch import Elasticsearch

from redis.asyncio import Redis as AsyncRedis

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from langchain.retrievers import EnsembleRetriever

from langchain_core.embeddings import Embeddings
from langchain_core.retrievers import BaseRetriever
from langchain_core.language_models import BaseChatModel
from langchain_core.vectorstores import VectorStoreRetriever

from langchain_gigachat import GigaChat
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_elasticsearch.vectorstores import ElasticsearchStore
from langchain_community.retrievers import ElasticSearchBM25Retriever

from langgraph.checkpoint.base import BaseCheckpointSaver

from .redis.async_saver import AsyncRedisCheckpointSaver
from .database.base import create_sessionmaker
from .database.repository import SQLMessageRepository
from .ai_agent.agent import RAGAgent

from .settings import Settings
from .base import AIAgent, MessageRepository
from .constants import VECTOR_STORE_INDEX, BM25_INDEX, SIMILARITY_WEIGHT, BM25_WEIGHT


class AppProvider(Provider):
    config = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_bot(self, config: Settings) -> Bot:
        return Bot(
            token=config.bot.TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
        )

    @provide(scope=Scope.APP)
    def get_embeddings(self, config: Settings) -> Embeddings:
        return HuggingFaceEmbeddings(
            model_name=config.embeddings.model_name,
            model_kwargs=config.embeddings.model_kwargs,
            encode_kwargs=config.embeddings.encode_kwargs,
        )

    @provide(scope=Scope.APP)
    def get_elastic(self, config: Settings) -> Elasticsearch:
        return Elasticsearch(
            hosts=config.elastic.elastic_url,
            basic_auth=(config.elastic.ELASTIC_USER, config.elastic.ELASTIC_PASSWORD),
            verify_certs=False
        )

    @provide(scope=Scope.APP)
    def get_redis(self, config: Settings) -> AsyncRedis:
        return AsyncRedis.from_url(config.redis.redis_url)

    @provide(scope=Scope.APP)
    def get_sessionmaker(self, config: Settings) -> async_sessionmaker[AsyncSession]:
        return create_sessionmaker(config.postgres)

    @provide(scope=Scope.APP)
    def get_bm25_retriever(self, elasticsearch: Elasticsearch) -> ElasticSearchBM25Retriever:
        return ElasticSearchBM25Retriever(
            client=elasticsearch,
            index_name=BM25_INDEX
        )

    @provide(scope=Scope.APP)
    def get_vector_store_retriever(self, embeddings: Embeddings, config: Settings) -> VectorStoreRetriever:
        return ElasticsearchStore(
            es_url=config.elasticsearch.elastic_url,
            es_user=config.elasticsearch.ELASTIC_USER,
            es_password=config.elasticsearch.ELASTIC_PASSWORD,
            index_name=VECTOR_STORE_INDEX,
            embedding=embeddings
        ).as_retriever()

    @provide(scope=Scope.APP)
    def get_retriever(
            self,
            vector_store_retriever: VectorStoreRetriever,
            bm25_retriever: ElasticSearchBM25Retriever
    ) -> BaseRetriever:
        return EnsembleRetriever(
            retrievers=[vector_store_retriever, bm25_retriever],
            weights=[SIMILARITY_WEIGHT, BM25_WEIGHT]
        )

    @provide(scope=Scope.APP)
    def get_model(self, config: Settings) -> BaseChatModel:
        return GigaChat(
            credentials=config.giga_chat.API_KEY,
            scope=config.giga_chat.SCOPE,
            profanity_check=False,
            verify_ssl_certs=False
        )

    @provide(scope=Scope.APP)
    def get_checkpoint_saver(self, redis: AsyncRedis) -> BaseCheckpointSaver:
        return AsyncRedisCheckpointSaver(redis)

    @provide(scope=Scope.APP)
    def get_message_repository(self, sessionmaker: async_sessionmaker[AsyncSession]) -> MessageRepository:
        return SQLMessageRepository(sessionmaker)

    @provide(scope=Scope.APP)
    def get_ai_agent(
            self,
            retriever: BaseRetriever,
            model: BaseChatModel,
            checkpointer: BaseCheckpointSaver
    ) -> AIAgent:
        return RAGAgent(retriever, model, checkpointer)


settings = Settings()

container = make_async_container(AppProvider(), context={Settings: settings})
