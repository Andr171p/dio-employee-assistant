from pathlib import Path

from elasticsearch import Elasticsearch
from langchain_community.retrievers import ElasticSearchBM25Retriever
from langchain_text_splitters import RecursiveCharacterTextSplitter


BASE_DIR: Path = Path(__file__).resolve().parent.parent

DOCUMENTS_DIR: Path = BASE_DIR / "documents"

elastic_client = Elasticsearch(
    hosts="https://localhost:9200",
    basic_auth=("elastic", "password"),
    verify_certs=False
)
info = elastic_client.info()
print(info)


directory = Path(DOCUMENTS_DIR)
files = directory.iterdir()

print("---Файлы в директории:---")
print(files)
print("---Чтение файлов---")

texts = []
for file in files:
    with open(file=file, mode='r', encoding='utf-8') as f:
        text = f.read()
        print(f"---Длина текста: {len(text)}---")
        print(text)
        texts.append(text)


text = '\n\n'.join(texts)

print(f"---Общая длина текста: {len(text)}---")


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=20,
    length_function=len
)

chunks = text_splitter.create_documents([text])

N = 5

print(f"Всего чанков: {len(chunks)}")
# print(f"Первые {N} чанков:")


indices = elastic_client.cat.indices(h='index').split()

# Удаление всех индексов
for index in indices:
    print(f"Удаляю индекс: {index}")
    elastic_client.indices.delete(index=index, ignore=[400, 404])

print("Все индексы удалены.")


bm25_retriever = ElasticSearchBM25Retriever(
    client=elastic_client,
    index_name="dio-consult",
    search_kwargs={"k": 5}
)

print("---Добавление документов в Elasticsearch...----")
bm25_retriever.add_texts([document.page_content for document in chunks])
print("---Добавление документов в Elasticsearch завершено---")