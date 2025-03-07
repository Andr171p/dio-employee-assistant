from elasticsearch import Elasticsearch
from langchain_community.retrievers import ElasticSearchBM25Retriever


elastic_client = Elasticsearch(
    hosts="https://localhost:9200",
    basic_auth=("elastic", "password"),
    verify_certs=False
)
info = elastic_client.info()
print(info)


bm25_retriever = ElasticSearchBM25Retriever(
    client=elastic_client,
    index_name="dio-consult",
    search_kwargs={"k": 5}
)

docs = bm25_retriever.invoke("Расскажи о заповедях ДИО-Консалт")
print(docs)
