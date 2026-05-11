# indexar.py
# indexação manual

from app.services.document_loader import load_all_documents
from app.services.chunking_service import create_chunks
from app.services.embedding_service import generate_embedding
from app.services.vector_store import save_chunks, save_vectors


all_chunks = []
all_vectors = []


documents = load_all_documents()

for document in documents:

    chunks = create_chunks(document["text"])

    for chunk in chunks:

        embedding = generate_embedding(chunk)

        all_chunks.append({
            "document": document["filename"],
            "text": chunk
        })

        all_vectors.append(embedding)

        print(f"Indexed chunk from {document['filename']}")


save_chunks(all_chunks)

save_vectors(all_vectors)

print("\nIndexing complete.")
