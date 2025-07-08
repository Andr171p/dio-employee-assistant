import os
import base64
import logging

import asynctempfile

from redis.asyncio import Redis
from elasticsearch import Elasticsearch

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langchain_core.retrievers import BaseRetriever
from langchain_core.language_models import BaseChatModel

from langchain.retrievers import EnsembleRetriever

from langchain_gigachat import GigaChat
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_elasticsearch import ElasticsearchStore
from langchain_community.retrievers import ElasticSearchBM25Retriever

from .states import RAGState
from .utils import format_messages, format_documents
from .templates import SUMMARIZATION_TEMPLATE, GENERATION_TEMPLATE, MULTIMODAL_GENERATION_TEMPLATE

from ..settings import settings
from ..constants import VECTOR_STORE_INDEX, BM25_INDEX, VECTOR_STORE_WEIGHT, BM25_WEIGHT

logger = logging.getLogger(__name__)

embeddings = HuggingFaceEmbeddings(
    model_name=settings.embeddings.MODEL_NAME,
    model_kwargs=settings.embeddings.MODEL_KWARGS,
    encode_kwargs=settings.embeddings.ENCODE_KWARGS,
)

elasticsearch_client = Elasticsearch(
    hosts=settings.elasticsearch.elastic_url,
    basic_auth=(settings.elasticsearch.ELASTIC_USER, settings.elasticsearch.ELASTIC_PASSWORD),
    verify_certs=False
)

redis = Redis.from_url(settings.redis.redis_url)

bm25_retriever = ElasticSearchBM25Retriever(client=elasticsearch_client, index_name=BM25_INDEX)

vector_store_retriever = ElasticsearchStore(
    es_url=settings.elasticsearch.elastic_url,
    es_user=settings.elasticsearch.ELASTIC_USER,
    es_password=settings.elasticsearch.ELASTIC_PASSWORD,
    index_name=VECTOR_STORE_INDEX,
    embedding=embeddings
)

retriever = EnsembleRetriever(
    retrievers=[vector_store_retriever, bm25_retriever],
    weights=[SIMILARITY_WEIGHT, BM25_WEIGHT]
)


async def summarize(state: RAGState) -> dict[str, str]:
    ...


async def retrieve(state: RAGState) -> dict[str, list[Document]]:
    ...


async def generate(state: RAGState) -> dict[str, list[BaseMessage]]:
    ...


class BaseNode(ABC):
    @abstractmethod
    async def __call__(self, state: TypedDict) -> Result: pass


class SummarizeNode(BaseNode):
    def __init__(self, model: BaseChatModel) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_chain = create_llm_chain(SUMMARIZATION_TEMPLATE, model)

    async def __call__(self, state: RAGState) -> Result:
        self.logger.info("---SUMMARIZE---")
        messages = state["messages"]
        question = messages[-1].content
        summary = await self.llm_chain.ainvoke({"messages": format_messages(messages)})
        question_with_summary = f"{summary}\n\n{question}"
        return {"question": question_with_summary}


class RetrieveNode(BaseNode):
    def __init__(self, retriever: BaseRetriever) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.retriever = retriever

    async def __call__(self, state: RAGState) -> Result:
        self.logger.info("---RETRIEVE---")
        documents = await self.retriever.ainvoke(state["question"])
        return {"documents": documents}


class GenerateNode(BaseNode):
    def __init__(self, model: BaseChatModel) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.llm_chain = create_llm_chain(GENERATION_TEMPLATE, model)

    async def __call__(self, state: RAGState) -> Result:
        self.logger.info("---GENERATE---")
        message = await self.llm_chain.ainvoke({
            "question": state["question"],
            "context": format_documents(state["documents"])
        })
        return {"messages": [message]}


class MultimodalGenerateNode(BaseNode):
    def __init__(self, model: GigaChat) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.model = model
        self.llm_chain = create_vision_llm_chain(MULTIMODAL_GENERATION_TEMPLATE, self.model)

    async def __call__(self, state: RAGState) -> Result:
        self.logger.info("---MULTIMODAL GENERATE---")
        documents = state["documents"]
        files: list[str] = []
        for document in documents:
            for image in document.metadata["images"]:
                async with asynctempfile.NamedTemporaryFile(
                        mode="wb", delete=False, suffix=".jpeg"
                ) as temp_file:
                    await temp_file.write(base64.b64decode(image["str_base64"]))
                    temp_file_path = temp_file.name

                with open(temp_file_path, mode="rb") as file:
                    uploaded_file = await self.model.aupload_file(file)
                os.unlink(temp_file_path)
                files.append(uploaded_file.id_)
        message = await self.llm_chain.ainvoke({
            "question": state["question"],
            "context": format_documents(documents),
            "history": files
        })
        return {"messages": [message]}
