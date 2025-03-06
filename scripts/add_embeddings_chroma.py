from pathlib import Path

import chromadb
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings


BASE_DIR: Path = Path(__file__).resolve().parent.parent

DOCUMENTS_DIR: Path = BASE_DIR / "documents"

CHROMA_DIR = BASE_DIR / "chroma"


client = chromadb.PersistentClient(path=str(CHROMA_DIR))
client.delete_collection("dio-consult")

print("---Коллекция dio-consult удалена---")


directory = Path(DOCUMENTS_DIR)
files = directory.iterdir()

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
print(f"Первые {N} чанков:")


embeddings = HuggingFaceEmbeddings(
    model_name="ai-forever/sbert_large_nlu_ru",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": False}
)


vector_store = Chroma.from_documents(
    collection_name="dio-consult",
    documents=chunks,
    embedding=embeddings,
    persist_directory=str(CHROMA_DIR)
)