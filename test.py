import asyncio
import logging

# from elasticsearch import Elasticsearch

from langchain_community.document_loaders import TextLoader
from langchain_community.retrievers import ElasticSearchBM25Retriever

from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.language_models import BaseChatModel

# from langchain_gigachat import GigaChat

from src.employee_assistant.dependencies import container
from src.employee_assistant.splitters import EnrichedMarkdownTextSplitter
from src.employee_assistant.document_loaders import (
    Docx2MdLoader,
    Pdf2MdLoader,
    Office2MdLoader
)

logger = logging.getLogger(__name__)


async def main() -> None:
    file_path = r"C:\Users\andre\IdeaProjects\DIORag\knowledge_base\Справочная информация\Услуги,_не_оказываемые_в_рамках_бесплатной_линии_консультаций.docx"
    extension = file_path.split(".")[-1]

    '''elastic = await container.get(Elasticsearch)
    indices = elastic.cat.indices(h="index").split()
    for index in indices:
        logger.info(f"Delete index: {index}")
        elastic.indices.delete(index=index, ignore=[400, 404])'''

    llm = await container.get(BaseChatModel)
    vector_store_retriever = await container.get(VectorStoreRetriever)
    bm25_retriever = await container.get(ElasticSearchBM25Retriever)

    text_splitter = EnrichedMarkdownTextSplitter(
        chunk_size=1024,
        chunk_overlap=50,
        length_function=len,
        llm=llm,
        use_md_headers_splitter=False,
        use_llm_for_ner=False
    )

    loader = TextLoader(file_path, encoding="utf-8")
    if extension in ("docx", "doc"):
        loader = Docx2MdLoader(file_path, use_md_table=True, include_images=False)
    elif extension == "pdf":
        loader = Pdf2MdLoader(file_path, include_images=False)
    elif extension in ("ppt", "pptx", "xls", "xlsx"):
        loader = Office2MdLoader(file_path)

    documents = loader.load_and_split(text_splitter)

    print(documents)

    vector_store_retriever.add_documents(documents)
    bm25_retriever.add_texts([document.page_content for document in documents])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
