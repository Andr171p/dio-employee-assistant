from langgraph.graph import START, StateGraph, END

from src.ai_agent.states import ReasoningState
from src.ai_agent.base_agent import BaseAgent
from src.ai_agent.nodes import (
    FirstStepNode,
    SearchNode,
    FinalizerNode,
    CritiqueNode,
    ReasonerNode,
    AnswerNode
)


class ReasoningAgent(BaseAgent):
    def __init__(
            self,
            first_step: FirstStepNode,
            search: SearchNode,
            finalize: FinalizerNode,
            critique: CritiqueNode,
            reason: ReasonerNode,
            answer: AnswerNode
    ) -> None:
        graph = StateGraph(ReasoningState)

        graph.add_node("think", reason)
        graph.add_node("first_step", first_step)
        graph.add_node("write", answer)
        graph.add_node("critic", critique)
        graph.add_node("search", search)
        graph.add_node("finalize", finalize)

        graph.add_edge(START, "think")
        graph.add_edge("think", "first_step")
        graph.add_edge("write", "critic")
        graph.add_edge("search", "write")
        graph.add_edge("finalize", END)

        self._graph_compiled = graph.compile()

    async def generate(self, question: str) -> ...:
        inputs = {"user_question": question}
        async for event in self._graph_compiled.astream_events(inputs, version="v2"):
            event_type = event.get('event', None)
            agent = event.get('name', '')
            if agent in ["_write", "RunnableSequence", "__start__", "__end__", "LangGraph"]:
                continue
            if event_type == 'on_chat_model_stream':
                print(event['data']['chunk'].content, end='')
            elif event_type == 'on_chain_start':
                print(f"<{agent}>")
            elif event_type == 'on_chain_end':
                print(f"</{agent}>")


'''from langchain.embeddings import HuggingFaceEmbeddings
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

search_node = SearchNode(retriever)
first_step_node = FirstStepNode(model)
reasoner_node = ReasonerNode(model)
critique_node = CritiqueNode(model)
answer_node = AnswerNode(model)
finalizer_node = FinalizerNode(model)

agent = ReasoningAgent(
    search=search_node,
    answer=answer_node,
    reason=reasoner_node,
    critique=critique_node,
    first_step=first_step_node,
    finalize=finalizer_node
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
    res = await agent.generate(questions[1])
    print(res)


asyncio.run(main())'''
