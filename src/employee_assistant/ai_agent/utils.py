from typing import Sequence

from pydantic import BaseModel

from langchain_core.documents import Document
from langchain_core.runnables import Runnable, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser

from langchain_gigachat import GigaChat


def format_documents(documents: list[Document]) -> str:
    """Приводит документы к удобному текстовому формату для LLM."""
    return "\n\n".join([document.page_content for document in documents])


def format_messages(messages: Sequence[BaseMessage]) -> str:
    """Приводит сообщения к удобному текстовому формату для LLM."""
    return "\n\n".join(
        f"{'User' if isinstance(message, HumanMessage) else 'AI'}: {message.content}"
        for message in messages
    )


def create_llm_chain(template: str, model: BaseChatModel) -> Runnable:
    """Создаёт LLM цепочку с инструкцией."""
    return (
        ChatPromptTemplate.from_template(template)
        | model
        | StrOutputParser()
    )


def create_structured_output_llm_chain(
        output_schema: type[BaseModel],
        template: str,
        model: BaseChatModel
) -> Runnable:
    """Создаёт LLM цепочку со структурным выводом."""
    parser = PydanticOutputParser(pydantic_object=output_schema)
    return (
        ChatPromptTemplate.from_messages(["system", template])
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


def create_vision_llm_chain(template: str, model: GigaChat) -> Runnable:
    """Создаёт LLM (GigaChat) цепочку с возможностью обрабатывать изображения."""
    return (
        RunnableLambda(_get_messages_from_file)
        | ChatPromptTemplate.from_messages([
            ("system", template),
            ("human", "Вопрос пользователя: {question}\n\nКонтекст: {context}"),
            MessagesPlaceholder("history")
        ])
        | model
        | StrOutputParser()
    )
