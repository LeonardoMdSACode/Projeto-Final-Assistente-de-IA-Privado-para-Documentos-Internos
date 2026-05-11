# test_loader.py

from app.services.document_loader import load_all_documents

documents = load_all_documents()

for doc in documents:

    print("=" * 50)
    print(doc["filename"])
    print(doc["text"][:500])
