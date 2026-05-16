# vector_store.py

import chromadb
import uuid

client = chromadb.PersistentClient(
    path="data/chroma_db"
)

collection = client.get_or_create_collection(
    name="documents"
)


def save_chunks(chunks):

    for chunk in chunks:

        text = chunk.get("text", "")

        if not isinstance(text, str):
            raise ValueError(f"Chunk text inválido: {type(text)}")

        embedding = chunk.get("embedding")

        if not isinstance(embedding, list):
            raise ValueError("Embedding inválido")

        collection.add(
            ids=[str(uuid.uuid4())],
            documents=[text],
            embeddings=[embedding],
            metadatas=[{
                "source": chunk.get("source", "UNKNOWN_SOURCE"),
                "doc_id": chunk.get("source", "UNKNOWN_DOC").split(".")[0],
                "chunk_id": chunk.get("chunk_id", -1),
                "snippet": chunk.get("snippet", text[:200]),
                "length": len(text)
            }]
        )


def search_chunks(query_embedding, top_k=10):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    formatted = []

    for i in range(len(docs)):

        meta = metas[i] if i < len(metas) else {}

        formatted.append({
            "text": docs[i],
            "source": meta.get("source") or "UNKNOWN_SOURCE",
            "snippet": meta.get("snippet") or docs[i][:200],
            "chunk_id": meta.get("chunk_id", -1),
            "distance": distances[i] if i < len(distances) else None
        })

    return formatted
