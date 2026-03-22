from elasticsearch import AsyncElasticsearch
from app.core.config import get_settings

settings = get_settings()
_elastic_search: AsyncElasticsearch | None = None

INDEX_MAPPINGS = {
    "mappings": {
        "properties": {
            "chunk_id": {"type": "keyword"},
            "doc_id": {"type": "keyword"},
            "title": {"type": "text", "analyzer": "english"},
            "content": {"type": "text", "analyzer":"english"},
            "source": {"type": "keyword" },
            "metadata": {"type": "object", "dynamic":True},
            "created_at": {"type": "Date"}
        }
    },
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
}

def get_es() -> AsyncElasticsearch:
    global _elastic_search
    if _elastic_search is None:
        _elastic_search = AsyncElasticsearch(
            hosts = [settings.elasticsearch_url],
            retry_on_timeout=True,
            max_retries=3
        )
    return _elastic_search

async def ensure_index() -> None:
    es = get_es()
    idx = settings.elasticsearch_index
    if not await es.indices.exists(index=idx):
        await es.indices.create(index=idx, body=INDEX_MAPPINGS)
        print(f"Created index {idx}")

async def bulk_index(docs: list[dict]) -> int:
    es = get_es()
    idx = settings.elasticsearch_index
    operations = []
    for doc in docs:
        operations.append({"index": {"index": idx, "_id": doc["chunk_id"]}})
        operations.append(doc)
    resp = await es.bulk(operations=operations, refresh=True)
    errors = [elem for elem in resp["items"] if "error" in elem.get("index", {})]
    return len(docs) - len(errors)

async def keyword_search(query: str, top_k: int) -> list[dict]:
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title^2", "content"],
                "type": "best_fields"
            }
        },
        "size": top_k
    }
    resp = await get_es().search(index=settings.elasticsearch_index, body=body)
    return [
        {"chunk_id": hit["_id"], "score": hit["_score"], **hit["_source"]}
        for hit in resp["hits"]["hits"]
    ]

async def delete_doc(doc_id: str) -> None:
    es = get_es()
    idx = settings.elasticsearch_index,
    await es.delete_by_query(
        index=idx,
        body={"query": {"term": {"doc_id":doc_id}}},
        refresh=True
    )

async def close_es() -> None:
    global _elastic_search
    if _elastic_search:
        await _elastic_search.close()
        _elastic_search = None
