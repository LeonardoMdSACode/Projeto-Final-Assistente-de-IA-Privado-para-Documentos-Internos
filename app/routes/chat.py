# app/routes/chat.py

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.retrieval_service import search
from app.services.llm_service import ask_llm
from app.services.memory_service import (
    add_message,
    get_history,
    clear_history
)
from app.services.query_rewrite_service import rewrite_query
from app.services.vector_store import collection

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


# -------------------------
# routing helpers
# -------------------------

def is_doc_list_query(q: str) -> bool:
    q = q.lower()
    return any(k in q for k in [
        "que documentos",
        "quais documentos",
        "lista de documentos",
        "o que tens na base de dados",
        "que ficheiros",
        "quais ficheiros"
    ])


def is_conversation_query(q: str) -> bool:
    q = q.lower()
    return any(k in q for k in [
        "falámos",
        "discutimos",
        "tema anterior",
        "isso",
        "explica melhor",
        "resume isso",
        "o que disseste"
    ])


@router.post("/chat")
def chat(request: ChatRequest):

    question = request.question

    add_message("user", question)

    history = get_history()

    formatted_history = "\n".join([
        f"{m['role']}: {m['content']}"
        for m in history[-6:]
    ])

    results = []
    answer = ""

    # ======================================================
    # MODE 1 — DOCUMENT LISTING (SEM RAG, SEM REWRITE)
    # ======================================================

    if is_doc_list_query(question):

        docs = collection.get(include=["metadatas"])

        unique_docs = sorted(set(
            m["source"] for m in docs["metadatas"]
        ))

        answer = "Documentos na base de dados:\n\n" + "\n".join(unique_docs)

        results = [{
            "source": "vector_db",
            "text": "\n".join(unique_docs)
        }]

    # ======================================================
    # MODE 2 — CONVERSA (SEM RAG)
    # ======================================================

    elif is_conversation_query(question):

        prompt = f"""
És um assistente com memória.

Usa apenas histórico da conversa.

Histórico:
{formatted_history}

Pergunta:
{question}
"""

        answer = ask_llm(prompt)

    # ======================================================
    # MODE 3 — RAG NORMAL
    # ======================================================

    else:

        rewritten = rewrite_query(question)

        results = search(rewritten, history=history)

        context = "\n\n---\n\n".join([
            f"[{r['source']}]\n{r['text']}"
            for r in results
        ]) if results else "SEM CONTEXTO DOCUMENTAL"

        prompt = f"""
És um assistente RAG.

REGRAS:
- usa apenas contexto fornecido
- nunca inventes
- se não houver informação diz:
  "Não encontrei essa informação nos documentos."

Histórico:
{formatted_history}

Contexto:
{context}

Pergunta:
{question}
"""

        answer = ask_llm(prompt)

    # -------------------------
    # memory update
    # -------------------------

    add_message("assistant", answer)

    # -------------------------
    # sources limpos (UI-safe)
    # -------------------------

    sources = sorted(set([
        r["source"] for r in results
    ])) if results else []

    return {
        "answer": answer,
        "sources": sources
    }


@router.post("/clear")
def clear_chat():
    clear_history()
    return {"message": "Histórico limpo."}
