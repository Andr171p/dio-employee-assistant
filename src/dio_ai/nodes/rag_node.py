from typing import Union

import chromadb
from langchain_chroma import Chroma
from elasticsearch import Elasticsearch
from langchain.prompts import ChatPromptTemplate
from langchain_core.embeddings import Embeddings
from langchain.retrievers import EnsembleRetriever
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

    async def execute(self, state: GraphState) -> dict:
        print("---RAG---")
        vector_store = Chroma(
            client=chromadb.PersistentClient(settings.chroma.persist_directory),
            collection_name=state.get("chapter"),
            embedding_function=self._embeddings
        )
        vector_store_retriever = vector_store.as_retriever()
        elastic_search = Elasticsearch(
            hosts=settings.elastic.url,
            basic_auth=(settings.elastic.user, settings.elastic.password),
            verify_certs=False
        )
        bm25_retriever = ElasticSearchBM25Retriever(
            client=elastic_search,
            index_name=state.get("chapter")
        )
        retriever = EnsembleRetriever(
            retrievers=[vector_store_retriever, bm25_retriever],
            weights=[0.6, 0.4]
        )
        prompt = ChatPromptTemplate.from_template(read_txt(RAG_TEMPLATE))
        parser = StrOutputParser()
        chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough()
            } |
            prompt |
            self._model |
            parser
        )
        final_answer = await chain.ainvoke(state["user_question"])
        return {"final_answer": final_answer}
