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
        collection.add(
            ids=[str(uuid.uuid4())],
            documents=[chunk["text"]],
            embeddings=[chunk["embedding"]],
            metadatas=[{
                "source": chunk["source"],
                "doc_id": chunk["source"].split(".")[0]
            }]
        )


def search_chunks(query_embedding, top_k=10):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    formatted = []

    for i in range(
        len(results["documents"][0])
    ):

        formatted.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"]
        })

    return formatted


def get_all_chunks(limit=20):

    results = collection.get(
        limit=limit,
        include=["documents", "metadatas"]
    )

    formatted = []

    for i in range(len(results["documents"])):

        formatted.append({
            "text": results["documents"][i],
            "source": results["metadatas"][i]["source"]
        })

    return formatted
