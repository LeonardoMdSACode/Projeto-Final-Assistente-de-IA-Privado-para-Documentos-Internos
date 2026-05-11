# chat.py
# endpoint /chat

from fastapi import APIRouter

router = APIRouter()

@router.post("/chat")
def chat(payload: dict):

    question = payload.get("question")

    return {
        "answer": f"Pergunta recebida: {question}"
    }
