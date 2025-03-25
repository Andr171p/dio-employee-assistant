from typing import Union

import chromadb
from langchain_chroma import Chroma
from elasticsearch import Elasticsearch
from langchain.vectorstores import VectorStore
from langchain.prompts import ChatPromptTemplate
from langchain_core.embeddings import Embeddings
from langchain.retrievers import EnsembleRetriever
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.language_models import BaseChatModel, LLM
from langchain_community.retrievers import ElasticSearchBM25Retriever

from src.dio_ai.state import GraphState
from src.config import BASE_DIR, settings
from src.misc.file_readers import read_txt
from src.utils.documents import format_docs
from src.dio_ai.nodes.base_node import BaseNode


RAG_TEMPLATE = BASE_DIR / "prompts" / "rag" / "ДИО_Консалт_сотрудник.txt"


class RAGNode(BaseNode):
    def __init__(
            self,
            embeddings: Embeddings,
            model: Union[BaseChatModel, LLM]
    ) -> None:
        self._embeddings = embeddings
        self._model = model

    def __create_vector_store(self, collection_name: str) -> VectorStore:
        return Chroma(
            client=chromadb.PersistentClient(settings.chroma.persist_directory),
            collection_name=collection_name,
            embedding_function=self._embeddings
        )

    @staticmethod
    def __get_elastic_search_client() -> Elasticsearch:
        return Elasticsearch(
            hosts=settings.elastic.url,
            basic_auth=(settings.elastic.user, settings.elastic.password),
            verify_certs=False
        )

    def _create_retriever(self, chapter: str) -> BaseRetriever:
        vector_store = self.__create_vector_store(chapter)
        vector_store_retriever = vector_store.as_retriever()
        elastic_search = self.__get_elastic_search_client()
        bm25_retriever = ElasticSearchBM25Retriever(
            client=elastic_search,
            index_name=chapter
        )
        return EnsembleRetriever(
            retrievers=[vector_store_retriever, bm25_retriever],
            weights=[0.6, 0.4]
        )

    async def execute(self, state: GraphState) -> dict:
        print("---RAG---")
        retriever = self._create_retriever(state.get("chapter"))
        prompt = ChatPromptTemplate.from_template(read_txt(RAG_TEMPLATE))
        chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough()
            } |
            prompt |
            self._model |
            StrOutputParser()
        )
        final_answer = await chain.ainvoke(state["user_question"])
        return {"final_answer": final_answer}
