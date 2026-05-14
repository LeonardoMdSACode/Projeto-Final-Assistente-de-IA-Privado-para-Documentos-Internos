from app.services.embedding_service import generate_embedding
from app.services.vector_store import search_chunks
from app.services.reranker_service import rerank
from app.services.query_rewrite_service import rewrite_query


def search(query, history=None):

    rewritten_query = rewrite_query(query)

    print("ORIGINAL:", query)
    print("REWRITTEN:", rewritten_query)

    query_embedding = generate_embedding(rewritten_query)

    results = search_chunks(query_embedding, top_k=10)

    results = rerank(rewritten_query, results)

    return results[:5]
