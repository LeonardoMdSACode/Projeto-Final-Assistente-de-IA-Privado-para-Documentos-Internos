# test_embedding.py

from app.services.embedding_service import generate_embedding

embedding = generate_embedding("O contrato termina em dezembro.")

print(len(embedding))
print(embedding[:10])
