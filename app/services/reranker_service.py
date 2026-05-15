# app/services/reranker_service.py

from sentence_transformers import CrossEncoder

# carrega 1x (import é lazy, mas isto fica em memória)
model = CrossEncoder("BAAI/bge-reranker-base")


def rerank(query, chunks, top_k=3):

    if not chunks:
        return []

    pairs = [
        (query, chunk["text"])
        for chunk in chunks
    ]

    scores = model.predict(pairs)

    ranked = sorted(
        zip(chunks, scores),
        key=lambda x: x[1],
        reverse=True
    )

    final = []

    for chunk, score in ranked[:top_k]:

        chunk["score"] = float(score)

        final.append(chunk)

    return final
