# retrieval_service.py

import numpy as np

from app.services.embedding_service import generate_embedding
from app.services.vector_store import load_chunks, load_vectors


def cosine_similarity(a, b):

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def search(query, top_k=3):

    query_embedding = generate_embedding(query)

    chunks = load_chunks()
    vectors = load_vectors()

    similarities = []

    for index, vector in enumerate(vectors):

        similarity = cosine_similarity(
            query_embedding,
            vector
        )

        similarities.append((similarity, index))

    similarities.sort(reverse=True)

    results = []

    for similarity, index in similarities[:top_k]:

        results.append({
            "score": float(similarity),
            "document": chunks[index]["document"],
            "text": chunks[index]["text"]
        })

    return results
