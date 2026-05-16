# llm_service.py

import requests


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

MODEL_NAME = "qwen2.5:3b"


def ask_llm(prompt: str):

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "num_predict": 400
                }
            },
            timeout=180
        )

        response.raise_for_status()

        data = response.json()

        text = data.get("response", "").strip()

        if not text:
            return "Não consegui gerar resposta."

        return text

    except Exception as e:

        print("[LLM ERROR]", e)

        return "Erro ao gerar resposta."
