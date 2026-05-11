# vector_store.py

import chromadb

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
            metadatas=[{"source": chunk["source"]}]
        )


def search_chunks(query_embedding, top_k=3):

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
