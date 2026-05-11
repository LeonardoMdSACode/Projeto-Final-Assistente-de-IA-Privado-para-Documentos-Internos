# chat.py
# endpoint /chat

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.retrieval_service import search
from app.services.llm_service import ask_llm

router = APIRouter()

class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
def chat(request: ChatRequest):

    results = search(request.question)

    context = "\n\n".join(
        [item["text"] for item in results]
    )

    prompt = f"""
Responde apenas com base no contexto.

Contexto:
{context}

Pergunta:
{request.question}
"""

    answer = ask_llm(prompt)

    return {
        "answer": answer,
        "sources": results
    }
