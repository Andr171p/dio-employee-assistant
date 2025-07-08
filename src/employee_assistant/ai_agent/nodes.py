import os
import base64
import logging
from PIL import Image
from io import BytesIO

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langchain_core.retrievers import BaseRetriever
from langchain_core.language_models import BaseChatModel

from langchain_gigachat import GigaChat

from .states import GraphState
from .utils import create_llm_chain, create_multimodal_llm_chain, format_documents, format_messages
from .prompts import SUMMARIZATION_PROMPT, GENERATION_PROMPT, MULTIMODAL_GENERATION_PROMPT

logger = logging.getLogger(__name__)


class SummarizeNode:
    def __init__(self, model: BaseChatModel) -> None:
        self.llm_chain = create_llm_chain(SUMMARIZATION_PROMPT, model)

    async def __call__(self, state: GraphState) -> dict[str, str]:
        logger.info("---SUMMARIZE---")
        messages = state["messages"]
        question = messages[-1].content
        summary = await self.llm_chain.ainvoke({"messages": format_messages(messages)})
        question_with_summary = f"{summary}\n\n{question}"
        return {"question": question_with_summary}


class RetrieveNode:
    def __init__(self, retriever: BaseRetriever) -> None:
        self.retriever = retriever

    async def __call__(self, state: GraphState) -> dict[str, list[Document]]:
        logger.info("---RETRIEVE---")
        documents = await self.retriever.ainvoke(state["question"])
        return {"documents": documents}


class GenerateNode:
    def __init__(self, model: BaseChatModel) -> None:
        self.llm_chain = create_llm_chain(GENERATION_PROMPT, model)

    async def __call__(self, state: GraphState) -> dict[str, list[BaseMessage | dict[str, str]]]:
        logger.info("---GENERATE---")
        message = await self.llm_chain.ainvoke({
            "question": state["question"],
            "context": format_documents(state["documents"])
        })
        return {"messages": [{"role": "ai", "content": message}]}


class MultimodalGenerateNode:
    def __init__(self, model: GigaChat) -> None:
        self.model = model
        self.llm_chain = create_multimodal_llm_chain(
            system_message=MULTIMODAL_GENERATION_PROMPT,
            prompt_template="Вопрос: {question}\n\nИнформация из контекста: {context}",
            model=model
        )

    async def __call__(self, state: GraphState) -> dict[str, list[BaseMessage | dict[str, str]]]:
        logger.info("---MULTIMODAL GENERATE---")
        documents = state["documents"]
        files: list[str] = []
        for document in documents:
            images = document.metadata.get("images")
            if not images:
                continue
            for image in images:
                str_base64 = image["str_base64"]
                data = base64.b64decode(str_base64.strip())
                image = Image.open(BytesIO(data))
                if image.mode == "RGBA":
                    image = image.convert("RGB")
                buffer = BytesIO()
                image.save(buffer, format="JPEG")
                buffer.seek(0)

                class NamedBytesIO(BytesIO):
                    name = "image.jpg"  # Это заставит GigaChat распознать тип

                named_buffer = NamedBytesIO(buffer.getvalue())

                uploaded_file = await self.model.aupload_file(named_buffer)
                files.append(uploaded_file.id_)
        message = await self.llm_chain.ainvoke({
            "question": state["question"],
            "context": format_documents(documents),
            "files": files
        })
        return {"messages": [{"role": "ai", "content": message}]}
