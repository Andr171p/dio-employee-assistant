import asyncio

from langchain_core.language_models import BaseChatModel

from src.employee_assistant.container import container
from src.employee_assistant.document_loaders import Docx2MdLoader
from src.employee_assistant.splitters.enriched import EnrichedMarkdownTextSplitter

file_path = r"C:\Users\andre\IdeaProjects\DIORag\knowledge_base\Инструкции\ИНСТРУКЦИЯ_1С_УФФ_АРМ_Специалиста.docx"

loader = Docx2MdLoader(docx_path=file_path, use_md_table=True, include_images=True)

NER_MODEL_NAME = "ru_core_news_md"


async def main() -> None:
    llm = await container.get(BaseChatModel)
    splitter = EnrichedMarkdownTextSplitter(
        chunk_size=500,
        chunk_overlap=20,
        length_function=len,
        header_to_split_on=[("#", "Header1"),],
        llm=llm,
        use_llm_for_ner=False,
        ner_model=NER_MODEL_NAME
    )
    docs = loader.load_and_split(splitter)
    print(docs[4])
    print(docs[4].metadata)


asyncio.run(main())
