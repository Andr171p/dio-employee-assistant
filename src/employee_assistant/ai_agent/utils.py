from typing import Sequence, Union, TypeVar

from uuid import UUID

from pydantic import BaseModel

from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import Runnable, RunnableLambda, RunnableConfig, RunnableParallel

from langchain_gigachat import GigaChat

from langgraph.graph.state import CompiledGraph

IdType = Union[str, int, UUID]

OutputSchema = TypeVar("OutputSchema", bound=BaseModel)


def format_documents(documents: list[Document]) -> str:
    """Convert documents into friendly text format for LLM."""
    return "\n\n".join([document.page_content for document in documents])


def format_messages(messages: Sequence[BaseMessage]) -> str:
    """Convert messages into friendly text format for LLM."""
    return "\n\n".join(
        f"{'User' if isinstance(message, HumanMessage) else 'AI'}: {message.content}"
        for message in messages
    )


def create_llm_chain(prompt_template: str, model: BaseChatModel) -> Runnable[dict[str, str], str]:
    return (
        ChatPromptTemplate.from_template(prompt_template)
        | model
        | StrOutputParser()
    )


def create_structured_output_llm_chain(
        output_schema: type[OutputSchema],
        prompt_template: str,
        model: BaseChatModel
) -> Runnable[dict[str, str], OutputSchema]:
    parser = PydanticOutputParser(pydantic_object=output_schema)
    return (
        ChatPromptTemplate.from_messages(["system", prompt_template])
        .partial(format_instructions=parser.get_format_instructions())
        | model
        | parser
    )


def _get_messages_from_file(urls: list[str]) -> dict[str, list[HumanMessage]]:
    return {
        "history":
            [
                HumanMessage(content="", additional_kwargs={"attachments": [url]})
                for url in urls
            ]
    }


def create_multimodal_llm_chain(prompt_template: str, model: GigaChat) -> Runnable:
    return (
        RunnableParallel({
            "question": lambda x: x["question"],
            "context": lambda x: x["context"],
            "history": RunnableLambda(_get_messages_from_file)
        })
        | ChatPromptTemplate.from_messages([
            ("system", prompt_template),
            ("human", "Вопрос пользователя: {question}\n\nКонтекст: {context}"),
            MessagesPlaceholder("history")
        ])
        | model
        | StrOutputParser()
    )


async def chat(thread_id: IdType, content: str, agent: CompiledGraph) -> str:
    config = RunnableConfig()
    config["configurable"] = {"thread_id": str(thread_id)}
    inputs = {"messages": [{"role": "human", "content": content}]}
    outputs = await agent.ainvoke(inputs, config=config)
    return outputs["messages"][-1]
