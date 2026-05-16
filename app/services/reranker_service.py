# app/services/reranker_service.py

from sentence_transformers import CrossEncoder

model = None

try:

    model = CrossEncoder(
        "BAAI/bge-reranker-base",
        local_files_only=True
    )

    print("[RERANKER] loaded")

except Exception as e:

    print("[RERANKER DISABLED]", e)

    model = None


def rerank(query, chunks, top_k=5):

    if not chunks:
        return []

    # fallback simples
    if model is None:

        for c in chunks:
            c["score"] = 0.0

        return chunks[:top_k]

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
