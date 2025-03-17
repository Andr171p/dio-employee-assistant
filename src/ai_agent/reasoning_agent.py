from pprint import pprint

from langgraph.graph import START, StateGraph, END

from src.ai_agent.states import GraphState
from src.ai_agent.base_agent import BaseAgent
from src.ai_agent.nodes import (
    DecisionNode,
    RetrieverNode,
    RewriterNode,
    GenerationNode
)


class ReasoningAgent(BaseAgent):
    def __init__(
            self,
            decision: DecisionNode,
            rewriter: RewriterNode,
            retriever: RetrieverNode,
            generation: GenerationNode,
    ) -> None:
        graph = StateGraph(GraphState)

        graph.add_node("start_step", decision)
        graph.add_node("rewrite", rewriter)
        graph.add_node("retrieve", retriever)
        graph.add_node("generate", generation)

        graph.add_edge(START, "start_step")
        graph.add_edge("rewrite", "retrieve")
        graph.add_edge("retrieve", "generate")
        graph.add_edge("generate", END)

        self._graph_compiled = graph.compile()

    async def generate(self, question: str) -> str:
        input = {"question": question}
        async for output in self._graph_compiled.astream(input):
            for key, value in output.items():
                pprint(f"Node '{key}':")
            pprint("\n---\n")
        pprint(value["answer"])
        return value["answer"]


from langchain.embeddings import HuggingFaceEmbeddings
from elasticsearch import Elasticsearch
from langchain_community.retrievers import ElasticSearchBM25Retriever
from langchain.retrievers import EnsembleRetriever
import chromadb
from langchain_chroma import Chroma
from langchain_gigachat import GigaChat
from src.config import settings


embeddings = HuggingFaceEmbeddings(
    model_name=settings.embeddings.model_name,
    model_kwargs=settings.embeddings.model_kwargs,
    encode_kwargs=settings.embeddings.encode_kwargs
)

vector_store = Chroma(
    client=chromadb.PersistentClient(settings.chroma.persist_directory),
    collection_name=settings.chroma.collection_name,
    embedding_function=embeddings
)

elastic = Elasticsearch(
    hosts=settings.elastic.url,
    basic_auth=(settings.elastic.user, settings.elastic.password),
    verify_certs=False
)

bm25_retriever = ElasticSearchBM25Retriever(
    client=elastic,
    index_name="dio-consult"
)

vector_store_retriever = vector_store.as_retriever()

retriever = EnsembleRetriever(
    retrievers=[vector_store_retriever, bm25_retriever],
    weights=[0.6, 0.4]
)

model = GigaChat(
    credentials=settings.giga_chat.api_key,
    scope=settings.giga_chat.scope,
    verify_ssl_certs=False,
    profanity_check=False
)

retriever_node = RetrieverNode(retriever)
generation_node = GenerationNode(model)
rewriter_node = RewriterNode(model)
decision_node = DecisionNode(model)

agent = ReasoningAgent(
    retriever=retriever_node,
    generation=generation_node,
    rewriter=rewriter_node,
    decision=decision_node
)

import asyncio

questions = [
    "Как уйти в оплачиваемый отпуск?",
    "Как взять отпуск используя 1с документооборот?",
    "Сколько зарабатывают новички",
    "Как совмещать работу и учебу?",
    "Что нельзя делать сотруднику",
    "Кто работает в отделе ЗУП"
]

async def main() -> None:
    res = await agent.generate(questions[-1])
    print(res)


asyncio.run(main())