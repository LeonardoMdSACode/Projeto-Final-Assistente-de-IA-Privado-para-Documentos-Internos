# indexar.py

from app.services.document_loader import load_all_documents
from app.services.chunking_service import create_chunks
from app.services.embedding_service import generate_embedding
from app.services.vector_store import save_chunks


def safe_truncate(text: str, max_chars=1800):
    return text if len(text) <= max_chars else text[:max_chars]


def run_indexing_pipeline():

    documents = load_all_documents()
    all_chunks = []

    for document in documents:

        chunks = create_chunks(document["text"])

        for chunk in chunks:

            text = chunk["text"]

            if len(text.strip()) < 30:
                continue

            text = safe_truncate(text)

            try:
                embedding = generate_embedding(text)
            except Exception as e:
                print(f"[EMBED ERROR] chunk={chunk['chunk_id']} err={e}")
                continue

            all_chunks.append({
                "text": text,
                "embedding": embedding,
                "source": document["source"],
                "chunk_id": chunk["chunk_id"],
                "snippet": chunk["snippet"]
            })

    print("TOTAL CHUNKS:", len(all_chunks))

    save_chunks(all_chunks)

    print("INDEXING DONE")


if __name__ == "__main__":
    run_indexing_pipeline()
