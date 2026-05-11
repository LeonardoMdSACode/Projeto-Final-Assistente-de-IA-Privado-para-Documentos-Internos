# indexar.py
# indexação manual

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

            embedding = generate_embedding(chunk)

            all_chunks.append({
                "text": chunk,
                "embedding": embedding,
                "source": document["source"]
            })

    print("CHUNKS:", len(all_chunks))
    print("EXEMPLO:", all_chunks[0])

    save_chunks(all_chunks)

    print("Indexação concluída")


if __name__ == "__main__":
    run_indexing_pipeline()
