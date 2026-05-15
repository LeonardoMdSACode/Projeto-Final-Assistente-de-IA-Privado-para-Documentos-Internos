# app/routes/chat.py

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.retrieval_service import search
from app.services.llm_service import ask_llm
from app.services.memory_service import add_message, get_history, clear_history
from app.services.query_rewrite_service import rewrite_query
from app.services.vector_store import collection

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


def is_greeting(q: str) -> bool:
    q = q.lower()
    return any(k in q for k in ["olá", "ola", "hello", "hi", "bom dia", "boa tarde", "boa noite"])


def is_doc_list_query(q: str) -> bool:
    q = q.lower()
    return any(k in q for k in ["que documentos", "quais documentos", "lista de documentos", "que ficheiros"])


def is_conversation_query(q: str) -> bool:
    q = q.lower()
    return any(k in q for k in ["falámos", "discutimos", "tema anterior", "isso", "explica melhor"])


@router.post("/chat")
def chat(request: ChatRequest):

    question = request.question
    add_message("user", question)

    history = get_history()

    formatted_history = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in history[-6:]
    )

    results = []
    answer = ""

    # ---------------- GREETING ----------------
    if is_greeting(question):

        answer = "Olá. Como posso ajudar?"
        results = []

    # ---------------- DOC LIST ----------------
    elif is_doc_list_query(question):

        docs = collection.get(include=["metadatas"])

        unique_docs = sorted(set(
            m.get("source", "UNKNOWN_SOURCE")
            for m in docs.get("metadatas", [])
        ))

        answer = "Documentos na base de dados:\n\n" + "\n".join(unique_docs)

        results = [
            {"source": d, "text": d, "snippet": d}
            for d in unique_docs
        ]

    # ---------------- CONVERSATION ----------------
    elif is_conversation_query(question):

        prompt = f"""
Histórico:
{formatted_history}

Pergunta:
{question}
"""

        answer = ask_llm(prompt)

    # ---------------- RAG ----------------
    else:

        rewritten = rewrite_query(question)
        results = search(rewritten, history=history)

        context = "\n\n====================\n\n".join([
            f"""
            SOURCE: {r['source']}
            CHUNK_ID: {r.get('chunk_id', -1)}
            RELEVANCE: {round(r.get('score', 0), 3)}

            CONTENT:
            {r['text']}
            """
            for i, r in enumerate(results)
        ])

        prompt = f"""
És um sistema RAG.

REGRAS CRÍTICAS:

1. Usa APENAS informação do contexto.
2. NÃO uses conhecimento externo.
3. Se contexto insuficiente:
   "Não encontrei essa informação nos documentos."
4. Cada afirmação deve incluir:
   - SOURCE
   - CHUNK_ID
5. Resume informação.
6. NÃO inventes detalhes.

FORMATO:

Resposta aqui.

FONTES USADAS:
- SOURCE | CHUNK_ID

-----------------------------------

CONTEXTO:

{context}

-----------------------------------

PERGUNTA:
{question}
"""

        answer = ask_llm(prompt)

    add_message("assistant", answer)

    # ---------------- SOURCES ----------------
    sources = [
        {
            "source": r.get("source", "UNKNOWN_SOURCE"),
            "snippet": r.get("snippet", "")
        }
        for r in results
    ]

    seen = set()
    unique_sources = []

    for s in sources:
        if s["source"] not in seen:
            seen.add(s["source"])
            unique_sources.append(s)

    chunks = [
        {
            "source": r.get("source", "UNKNOWN_SOURCE"),
            "text": r.get("text", ""),
            "snippet": r.get("snippet", r.get("text", "")[:200]),
            "chunk_id": r.get("chunk_id", -1)
        }
        for r in results
    ]

    return {
        "answer": answer,
        "sources": unique_sources,
        "chunks": chunks
    }


@router.post("/clear")
def clear_chat():
    clear_history()
    return {"message": "Histórico limpo."}
