from pprint import pprint

from langgraph.graph import START, StateGraph, END

from src.ai_graph.states import GraphState
from src.ai_graph.nodes import RetrieverNode, GenerationNode, RewriterNode


class Workflow:
    def __init__(
            self,
            retriever_node: RetrieverNode,
            generation_node: GenerationNode,
            rewriter_node: RewriterNode
    ) -> None:
        workflow = StateGraph(GraphState)
        workflow.add_node("retrieve", retriever_node.retrieve)
        workflow.add_node("rewrite", rewriter_node.rewrite)
        workflow.add_node("generate", generation_node.generate)
        workflow.add_edge(START, "retrieve")
        workflow.add_edge("retrieve", "rewrite")
        workflow.add_edge("rewrite", "generate")
        workflow.add_edge("generate", END)
        self._app = workflow.compile()

    def execute(self, question: str) -> str:
        inputs = {"question": question}
        for output in self._app.stream(inputs):
            for key, value in output.items():
                pprint(f"Node '{key}':")
            pprint("\n---\n")
        pprint(value["generation"])
        return value["generation"]


from langchain.embeddings import HuggingFaceEmbeddings
from elasticsearch import Elasticsearch
from langchain_community.retrievers import ElasticSearchBM25Retriever
from langchain.retrievers import EnsembleRetriever
import chromadb
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_gigachat import GigaChat
from langchain_core.output_parsers.string import StrOutputParser

from src.misc.file_readers import read_txt
from src.config import settings


embeddings = HuggingFaceEmbeddings(
    model_name=settings.embeddings.model_name,
    model_kwargs=settings.embeddings.model_kwargs,
    encode_kwargs=settings.embeddings.encode_kwargs
)

vector_store = Chroma(
    client=chromadb.PersistentClient(settings.chroma.persist_directory),
    collection_name=settings.chroma.collection_name,
    embedding_function=embeddings
)

elastic = Elasticsearch(
    hosts=settings.elastic.url,
    basic_auth=(settings.elastic.user, settings.elastic.password),
    verify_certs=False
)

bm25_retriever = ElasticSearchBM25Retriever(
    client=elastic,
    index_name="dio-consult"
)

vector_store_retriever = vector_store.as_retriever()

retriever = EnsembleRetriever(
    retrievers=[vector_store_retriever, bm25_retriever],
    weights=[0.6, 0.4]
)

model = GigaChat(
    credentials=settings.giga_chat.api_key,
    scope=settings.giga_chat.scope,
    verify_ssl_certs=False,
    profanity_check=False
)

parser = StrOutputParser()

rag_prompt = ChatPromptTemplate.from_template(read_txt(settings.prompts.rag_prompt))
rewriter_prompt = ChatPromptTemplate.from_template(read_txt(settings.prompts.rewriter_prompt))

retriever_node = RetrieverNode(retriever)
generation_node = GenerationNode(rag_prompt, model, parser)
rewriter_node = RewriterNode(rewriter_prompt, model, parser)

ai = Workflow(
    retriever_node=retriever_node,
    generation_node=generation_node,
    rewriter_node=rewriter_node
)
res = ai.execute("Как правильно заполнять письмо?")
print(res)