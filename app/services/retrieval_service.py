# retrieval_service.py

import numpy as np

from app.services.embedding_service import generate_embedding
from app.services.vector_store import search_chunks


def search(query):

    query_embedding = generate_embedding(query)

    results = search_chunks(query_embedding)

    print("RESULTADOS RETRIEVAL:", results)

    return results
