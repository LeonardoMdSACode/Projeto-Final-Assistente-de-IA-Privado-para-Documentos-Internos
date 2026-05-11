# embedding_service.py
# embeddings Ollama

import requests


OLLAMA_URL = "http://127.0.0.1:11434/api/embeddings"

EMBED_MODEL = "nomic-embed-text"


def generate_embedding(text):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": EMBED_MODEL,
            "prompt": text
        }
    )

    data = response.json()

    return data["embedding"]
