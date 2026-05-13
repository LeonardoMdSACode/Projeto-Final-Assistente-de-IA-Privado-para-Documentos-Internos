# retrieval_service.py

import numpy as np

from app.services.embedding_service import generate_embedding
from app.services.vector_store import search_chunks


def search(query, document=None):

    query_embedding = generate_embedding(query)

    print("\nPERGUNTA:")
    print(query)

    print("\nTAMANHO EMBEDDING:")
    print(len(query_embedding))

    results = search_chunks(
        query_embedding,
        document=document
    )

    print("\nRESULTADOS RETRIEVAL:")

    for i, result in enumerate(results):

        print(f"\n--- RESULTADO {i+1} ---")
        print("SOURCE:", result["source"])
        print("TEXT:")
        print(result["text"][:1000])

    return results
