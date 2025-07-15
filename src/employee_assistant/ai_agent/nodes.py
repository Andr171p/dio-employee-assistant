import base64
import logging
from PIL import Image
from io import BytesIO
from uuid import uuid4

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.language_models import BaseChatModel

from langchain_gigachat import GigaChat

from .states import GraphState
from .utils import create_llm_chain, create_gigachat_llm_chain, format_documents, format_messages
from .prompts import SUMMARIZATION_PROMPT, GENERATION_PROMPT, GIGACHAT_SYSTEM_PROMPT, QA_PROMPT

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
        logger.info(documents)
        return {"documents": documents}


class GenerateNode:
    def __init__(self, model: BaseChatModel) -> None:
        self.llm_chain = create_llm_chain(GENERATION_PROMPT, model)

    async def __call__(self, state: GraphState) -> dict[str, list[dict[str, str]]]:
        logger.info("---GENERATE---")
        message = await self.llm_chain.ainvoke({
            "question": state["question"],
            "context": format_documents(state["documents"])
        })
        return {"messages": [{"role": "ai", "content": message}]}


class GenerateWithFilesNode:
    def __init__(self, model: GigaChat) -> None:
        self.model = model
        self.llm_chain = create_gigachat_llm_chain(
            system_message=GIGACHAT_SYSTEM_PROMPT,
            prompt_template=QA_PROMPT,
            model=model
        )

    async def __call__(self, state: GraphState) -> dict[str, list[dict[str, str]]]:
        logger.info("---GENERATE---")
        documents = state["documents"]
        files: list[str] = []
        for document in documents:
            images = document.metadata.get("images")
            if not images:
                continue
            for image in images:
                str_base64 = image["str_base64"]
                file_buffer = self._open_buffered_image(str_base64, f"{uuid4()}.jpg")
                uploaded_file = await self.model.aupload_file(file_buffer)
                files.append(uploaded_file.id_)
        message = await self.llm_chain.ainvoke({
            "question": state["question"],
            "context": format_documents(documents),
            "files": files
        })
        return {"messages": [{"role": "ai", "content": message}]}

    @staticmethod
    def _open_buffered_image(base64_str: str, file_name: str) -> BytesIO:
        data = base64.b64decode(base64_str.strip())
        image = Image.open(BytesIO(data))
        if image.mode == "RGBA":
            image = image.convert("RGB")
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)
        buffer.name = file_name
        return buffer
