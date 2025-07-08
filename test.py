import asyncio
import base64
import tempfile
import os

from langchain.document_loaders import TextLoader

# from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.documents import Document

from langchain_gigachat import GigaChat

# from langchain_community.retrievers import ElasticSearchBM25Retriever

from src.employee_assistant.container import container
from src.employee_assistant.splitters import EnrichedMarkdownTextSplitter
from src.employee_assistant.document_loaders import (
    Docx2MdLoader,
    Pdf2MdLoader,
    Office2MdLoader
)


async def main() -> None:
    file_path = r"C:\Users\andre\IdeaProjects\DIORag\knowledge_base\Инструкции\ИНСТРУКЦИЯ_1С_УФФ_АРМ_Специалиста.docx"
    extension = file_path.split(".")[-1]

    llm = await container.get(GigaChat)
    # vector_store_retriever = await container.get(VectorStoreRetriever)
    # bm25_retriever = await container.get(ElasticSearchBM25Retriever)

    text_splitter = EnrichedMarkdownTextSplitter(
        chunk_size=600,
        chunk_overlap=20,
        length_function=len,
        header_to_split_on=[("#", "Header1"),],
        llm=llm,
        use_llm_for_ner=False
    )

    loader = TextLoader(file_path)
    if extension in ("docx", "doc"):
        loader = Docx2MdLoader(file_path, use_md_table=True, include_images=True)
    elif extension == "pdf":
        loader = Pdf2MdLoader(file_path, include_images=True)
    elif extension in ("ppt", "pptx", "xls", "xlsx"):
        loader = Office2MdLoader(file_path)

    documents = loader.load_and_split(text_splitter)

    # vector_store_retriever.add_documents(documents)
    # bm25_retriever.add_texts([document.page_content for document in documents])

    image = documents[4].metadata["images"][0]
    print("Images count: ", len(documents[4].metadata["images"]))

    with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".jpeg") as tmp:
        tmp.write(base64.b64decode(image["str_base64"]))
        tmp_path = tmp.name

    with open(tmp_path, "rb") as file:
        uploaded_file = llm.upload_file(file)
    print(uploaded_file.id_)
    os.unlink(tmp_path)
    response = llm.invoke([
        SystemMessage(content="Ты - ассистент, который анализирует изображения и текст."),
        HumanMessage(
            content=documents[4].page_content,
            additional_kwargs={"attachments": [uploaded_file.id_]},
        )
    ])
    print(response.content)


if __name__ == "__main__":
    asyncio.run(main())
