# app/services/retrieval_service.py

from app.services.embedding_service import generate_embedding
from app.services.vector_store import search_chunks
from app.services.reranker_service import rerank

MIN_SCORE = -0.3


def deduplicate_chunks(results):

    seen = set()

    final = []

    for r in results:

        text = r["text"][:300]

        if text in seen:
            continue

        seen.add(text)

        final.append(r)

    return final


def search(query, history=None):

    query_embedding = generate_embedding(query)

    results = search_chunks(
        query_embedding,
        top_k=20
    )

    if not results:
        return []

    results = deduplicate_chunks(results)

    ranked = rerank(
        query,
        results,
        top_k=6
    )

    filtered = []

    for r in ranked:

        score = r.get("score", 0)

        if score >= MIN_SCORE:
            filtered.append(r)

    return filtered
