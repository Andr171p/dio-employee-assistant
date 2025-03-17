from typing import List

import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_gigachat import GigaChat
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from langchain_community.chat_message_histories.redis import RedisChatMessageHistory


embeddings = HuggingFaceEmbeddings(
    model_name="ai-forever/sbert_large_nlu_ru",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": False}
)

client = chromadb.PersistentClient(r"C:\Users\andre\IdeaProjects\DIORag\chroma")
vector_store = Chroma(
    client=client, 
    collection_name="dio-consult",
    embedding_function=embeddings
)

retriever = vector_store.as_retriever()


def format_docs(documents: List[Document]) -> str:
    return "\n\n".join([document.page_content for document in documents])


GIGACHAT_API_KEY = "OTAyMDdkMDItNTQ4Yi00YWViLTk4YjYtYjBhMTE4ZTI1MDJmOjUxOTFjYzk2LWExNWItNDZkMS1hZDdjLWI0N2M4OWU0NDJhZg=="
GIGACHAT_SCOPE = "GIGACHAT_API_PERS"

PROMPT_PATH = r"/prompts/ДИО_Консалт_сотрудник.txt"

with open(PROMPT_PATH, encoding="utf-8") as file:
    template = file.read()

prompt = ChatPromptTemplate.from_template(template)


model = GigaChat(
    credentials=GIGACHAT_API_KEY,
    scope=GIGACHAT_SCOPE,
    verify_ssl_certs=False,
    profanity_check=False
)


parser = StrOutputParser()


rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    } |
    prompt |
    model |
    parser
)


while True:
    question = input("Запрос в RAG: ")
    if question == "exit":
        break
    res = rag_chain.invoke(question)
    print(res)
