# test_chunking.py

from app.services.document_loader import load_all_documents
from app.utils.chunking import create_chunks

documents = load_all_documents()

for doc in documents:

    chunks = create_chunks(doc["text"])

    print("\n")
    print(doc["filename"])
    print("Chunks:", len(chunks))
    print(chunks[0][:300])
