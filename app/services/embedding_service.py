# embedding_service.py
# embeddings Ollama

import requests


OLLAMA_URL = "http://127.0.0.1:11434/api/embeddings"

EMBED_MODEL = "bge-m3"


def generate_embedding(text: str):

    payload = {
        "model": EMBED_MODEL,
        "prompt": text
    }

    response = requests.post(OLLAMA_URL, json=payload)

    # fail hard com contexto útil
    if response.status_code != 200:
        raise RuntimeError(
            f"Ollama embedding failed: {response.text}"
        )

    data = response.json()

    # DEBUG
    print("EMBEDDING RESPONSE KEYS:", data.keys())

    embedding = data.get("embedding")

    if not embedding:
        raise KeyError(f"Embedding não encontrado. Response: {data}")

    return embedding
