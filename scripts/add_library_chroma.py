from pathlib import Path

import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_DIR = BASE_DIR / "chroma"

client = chromadb.PersistentClient(path=str(CHROMA_DIR))
try:
    client.delete_collection("products-1c")
    client.delete_collection("beginners")
except Exception as ex:
    print(ex)

LIBRARY_DIR = BASE_DIR / "documents_library"

DIR_DIO = LIBRARY_DIR / "Дио-Консалт"
DIR_INSTRUCTIONS = LIBRARY_DIR / "Инструкции"
DIR_COMMERCIAL = LIBRARY_DIR / "Коммерческие_предложения"
DIR_INFO = LIBRARY_DIR / "Общая_информация"


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


embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-large",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": False}
)


def create_vector_store_index(name: str, chunks: list[Document]) -> None:
    vector_store = Chroma.from_documents(
        collection_name=name,
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR)
    )
    print(f"Данные добавлены в {name}")


texts = {
    "dio-consult": get_dio_text(),
    "instructions": get_instructions_text(),
    "commercial": get_commercial_text(),
    "info": get_info_text()
}

for name, text in texts.items():
    client.delete_collection(name)
    print(f"Коллекция {name} удалена")
    print(len(text))
    chunks = create_chunks(text)
    create_vector_store_index(name, chunks)
