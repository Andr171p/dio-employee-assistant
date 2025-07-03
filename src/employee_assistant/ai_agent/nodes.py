from typing import Union
from typing_extensions import TypedDict

from abc import ABC, abstractmethod
import logging

from langgraph.types import Command

from langchain_core.retrievers import BaseRetriever
from langchain_core.language_models import BaseChatModel

from .states import RAGState
from .utils import create_llm_chain, format_messages, format_documents
from .templates import SUMMARIZATION_TEMPLATE, GENERATION_TEMPLATE

Result = Union[dict, Command]


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
