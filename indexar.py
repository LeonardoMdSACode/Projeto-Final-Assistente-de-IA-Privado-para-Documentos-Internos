# indexar.py

from app.services.document_loader import load_all_documents
from app.services.chunking_service import create_chunks
from app.services.embedding_service import generate_embedding
from app.services.vector_store import save_chunks


def run_indexing_pipeline():

    documents = load_all_documents()

    all_chunks = []

    for document in documents:

        chunks = create_chunks(document["text"])

        for chunk in chunks:

            text = chunk["text"]

            embedding = generate_embedding(text)

            all_chunks.append({
                "text": chunk["text"],
                "embedding": embedding,
                "source": document["source"],
                "chunk_id": chunk.get("chunk_id", -1),
                "snippet": chunk["text"][:300]
            })

    print("CHUNKS:", len(all_chunks))

    if all_chunks:
        print("EXEMPLO:", all_chunks[0])

    save_chunks(all_chunks)

    print("Indexação concluída")
