# llm_service.py

import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

MODEL_NAME = "qwen2.5:3b"


def ask_llm(prompt: str):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data["response"]
