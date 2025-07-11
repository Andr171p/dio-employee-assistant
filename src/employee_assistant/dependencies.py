from collections.abc import AsyncIterator

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
from langchain_core.vectorstores import VectorStore
from langchain_core.language_models import BaseChatModel
from langchain_core.vectorstores import VectorStoreRetriever

from langchain_gigachat import GigaChat
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_elasticsearch import ElasticsearchStore
from langchain_community.retrievers import ElasticSearchBM25Retriever

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledGraph

from .redis.async_saver import AsyncRedisCheckpointSaver
from .database.base import create_sessionmaker

from .ai_agent.workflow import build_graph
from .ai_agent.nodes import SummarizeNode, RetrieveNode, GenerateNode

from .settings import Settings
from .constants import (
    VECTOR_STORE_INDEX,
    BM25_INDEX,
    VECTOR_STORE_RETRIEVER_WEIGHT,
    BM25_RETRIEVER_WEIGHT,
    TIMEOUT
)


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
            model_name=config.embeddings.MODEL_NAME,
            model_kwargs=config.embeddings.MODEL_KWARGS,
            encode_kwargs=config.embeddings.ENCODE_KWARGS,
        )

    @provide(scope=Scope.APP)
    def get_elastic(self, config: Settings) -> Elasticsearch:
        print(config.elasticsearch.elastic_url)
        return Elasticsearch(
            # hosts=config.elasticsearch.elastic_url,
            hosts=["http://elastic:9200"],
            basic_auth=(config.elasticsearch.ELASTIC_USER, config.elasticsearch.ELASTIC_PASSWORD),
            # verify_certs=False
        )

    @provide(scope=Scope.APP)
    def get_redis(self, config: Settings) -> AsyncRedis:
        return AsyncRedis.from_url(config.redis.redis_url)

    @provide(scope=Scope.APP)
    def get_sessionmaker(self, config: Settings) -> async_sessionmaker[AsyncSession]:
        return create_sessionmaker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(
            self, sessionmaker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AsyncSession]:
        async with sessionmaker() as session:
            yield session

    @provide(scope=Scope.APP)
    def get_bm25_retriever(self, elasticsearch: Elasticsearch) -> ElasticSearchBM25Retriever:
        return ElasticSearchBM25Retriever(
            client=elasticsearch,
            index_name=BM25_INDEX
        )

    @provide(scope=Scope.APP)
    def get_vector_store(self, embeddings: Embeddings, elasticsearch: Elasticsearch) -> VectorStore:
        return ElasticsearchStore(
            es_connection=elasticsearch,
            index_name=VECTOR_STORE_INDEX,
            embedding=embeddings
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
            weights=[VECTOR_STORE_RETRIEVER_WEIGHT, BM25_RETRIEVER_WEIGHT]
        )

    @provide(scope=Scope.APP)
    def get_model(self, config: Settings) -> BaseChatModel:
        return GigaChat(
            credentials=config.giga_chat.API_KEY,
            scope=config.giga_chat.SCOPE,
            model=config.giga_chat.MODEL_NAME,
            profanity_check=False,
            verify_ssl_certs=False,
            timeout=TIMEOUT
        )

    @provide(scope=Scope.APP)
    def get_checkpoint_saver(self, redis: AsyncRedis) -> BaseCheckpointSaver:
        return AsyncRedisCheckpointSaver(redis)

    @provide(scope=Scope.APP)
    def get_agent(
            self,
            retriever: BaseRetriever,
            model: GigaChat,
            checkpointer: BaseCheckpointSaver
    ) -> CompiledGraph:
        return build_graph(
            summarize_node=SummarizeNode(model),
            retrieve_node=RetrieveNode(retriever),
            generate_node=GenerateNode(model),
            checkpointer=checkpointer
        )


settings = Settings()

container = make_async_container(AppProvider(), context={Settings: settings})
