# app/services/retrieval_service.py

from app.services.embedding_service import generate_embedding
from app.services.vector_store import search_chunks
from app.services.reranker_service import rerank

# filtro menos agressivo (evita matar recall)
MIN_SCORE = -1.0


def deduplicate_chunks(results):
    seen = set()
    final = []

    for r in results:
        key = r["text"][:300]

        if key in seen:
            continue

        seen.add(key)
        final.append(r)

    return final


def search(query, history=None):

    # NÃO usar history aqui ainda (evita ruído no embedding)
    query_embedding = generate_embedding(query)

    results = search_chunks(
        query_embedding,
        top_k=25
    )

    if not results:
        return []

    results = deduplicate_chunks(results)

    ranked = rerank(
        query,
        results,
        top_k=8
    )

    # IMPORTANT: não matar resultados cedo demais
    filtered = []

    for r in ranked:
        score = r.get("score", 0)

        if score >= MIN_SCORE:
            filtered.append(r)

    # fallback safety: nunca devolver vazio se há candidatos
    if not filtered and ranked:
        return ranked[:3]

    return filtered
