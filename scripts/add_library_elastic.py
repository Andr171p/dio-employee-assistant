from pathlib import Path

from langchain_core.documents import Document
from elasticsearch import Elasticsearch
from langchain_community.retrievers import ElasticSearchBM25Retriever
from langchain_text_splitters import RecursiveCharacterTextSplitter


BASE_DIR = Path(__file__).resolve().parent.parent

LIBRARY_DIR = BASE_DIR / "documents_library"

DIR_1C = LIBRARY_DIR / "1С"
DIR_DIO = LIBRARY_DIR / "Дио-Консалт"
DIR_INSTRUCTIONS = LIBRARY_DIR / "Инструкции"
DIR_COMMERCIAL = LIBRARY_DIR / "Коммерческие_предложения"
DIR_NEW = LIBRARY_DIR / "Новичкам"
DIR_INFO = LIBRARY_DIR / "Общая_информация"


elastic_client = Elasticsearch(
    hosts="https://localhost:9200",
    basic_auth=("elastic", "password"),
    verify_certs=False
)
info = elastic_client.info()
print(info)

indices = elastic_client.cat.indices(h='index').split()

# Удаление всех индексов
for index in indices:
    print(f"Удаляю индекс: {index}")
    elastic_client.indices.delete(index=index, ignore=[400, 404])

print("Все индексы удалены.")


def get_dio_text() -> str:
    files = DIR_DIO.iterdir()
    texts = []
    for file in files:
        with open(file=file, mode="r", encoding="utf-8") as f:
            text = f.read()
            texts.append(text)
    return '\n\n'.join(texts)


def get_instructions_text() -> str:
    files = DIR_INSTRUCTIONS.iterdir()
    texts = []
    for file in files:
        with open(file=file, mode="r", encoding="utf-8") as f:
            text = f.read()
            texts.append(text)
    return '\n\n'.join(texts)


def get_commercial_text() -> str:
    files = DIR_COMMERCIAL.iterdir()
    texts = []
    for file in files:
        with open(file=file, mode="r", encoding="utf-8") as f:
            text = f.read()
            texts.append(text)
    return '\n\n'.join(texts)


def get_info_text() -> str:
    files = DIR_INFO.iterdir()
    texts = []
    for file in files:
        with open(file=file, mode="r", encoding="utf-8") as f:
            text = f.read()
            texts.append(text)
    return '\n\n'.join(texts)


text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=20,
        length_function=len
)


def create_chunks(text: str) -> list[Document]:
    chunks = text_splitter.create_documents([text])
    print(f"Всего чанков: {len(chunks)}")
    return chunks


def create_elastic_index(name: str, chunks: list[Document]) -> None:
    bm25_retriever = ElasticSearchBM25Retriever(
        client=elastic_client,
        index_name=name,
        search_kwargs={"k": 5}
    )

    print("---Добавление документов в Elasticsearch...----")
    bm25_retriever.add_texts([document.page_content for document in chunks])
    print("---Добавление документов в Elasticsearch завершено---")


texts = {
    "dio-consult": get_dio_text(),
    "instructions": get_instructions_text(),
    "commercial": get_commercial_text(),
    "info": get_info_text()
}

for name, text in texts.items():
    print(len(text))
    chunks = create_chunks(text)
    create_elastic_index(name, chunks)
