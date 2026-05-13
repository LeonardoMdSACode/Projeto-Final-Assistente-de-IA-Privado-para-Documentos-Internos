# chat.py
# endpoint /chat

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.retrieval_service import search
from app.services.llm_service import ask_llm
from app.services.vector_store import get_all_chunks

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    document: str | None = None


@router.post("/chat")
def chat(request: ChatRequest):

    question = request.question.lower()

    if "resume" in question or "sobre o que" in question:

        results = get_all_chunks(limit=20)

    else:

        question = request.question.lower()

        if "resume" in question or "sobre o que" in question:
        
            results = get_all_chunks(limit=20)

        else:
        
            results = search(
                request.question,
                document=request.document
            )

    context = "\n\n".join(
        [item["text"] for item in results]
    )

    prompt = f"""
És um assistente RAG.

Responde APENAS usando o contexto fornecido.

Se a pergunta pedir um resumo do documento,
tenta identificar:
- tema principal
- tecnologias
- objetivos
- tópicos recorrentes

Não inventes informação.

CONTEXTO:
{context}

PERGUNTA:
{request.question}

RESPOSTA:
"""

    print("\nCONTEXTO FINAL:")
    print(context[:3000])

    print("\nPROMPT FINAL:")
    print(prompt[:4000])
    
    answer = ask_llm(prompt)

    return {
        "answer": answer,
        "sources": results
    }
