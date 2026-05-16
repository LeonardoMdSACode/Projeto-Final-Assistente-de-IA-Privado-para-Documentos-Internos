# app/routes/chat.py

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.retrieval_service import search
from app.services.llm_service import ask_llm
from app.services.memory_service import add_message, get_history
from app.services.vector_store import collection

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


def is_greeting(q: str) -> bool:
    q = q.lower()
    return any(k in q for k in ["olá", "ola", "hello", "hi"])


def is_doc_list_query(q: str) -> bool:
    q = q.lower()
    return any(k in q for k in [
        "que documentos",
        "quais documentos",
        "lista de documentos"
    ])


@router.post("/chat")
def chat(request: ChatRequest):

    question = request.question
    add_message("user", question)

    history = get_history()

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

        answer = "Documentos:\n\n" + "\n".join(unique_docs)
        results = []

    # ---------------- RAG + MEMORY ----------------
    else:

        results = search(question)

        print("RAG RESULTS COUNT:", len(results))
        print("RAG SAMPLE:", results[:1])

        context = "\n\n---\n\n".join(
            f"SOURCE: {r['source']}\nCHUNK_ID: {r.get('chunk_id', -1)}\nTEXT:\n{r['text']}"
            for r in results
        )

        formatted_history = "\n".join(
            f"{m['role']}: {m['content']}"
            for m in history[-6:]
        )

        prompt = f"""
Tu és um assistente RAG.

REGRAS:
- usa histórico + documentos
- nunca inventes
- se não souberes diz explicitamente

HISTÓRICO:
{formatted_history}

DOCUMENTOS:
{context}

PERGUNTA:
{question}

RESPOSTA:
"""

        answer = ask_llm(prompt)

    add_message("assistant", answer)

    # 🔥 IMPORTANTE: agora devolve sources reais
    unique_sources = []
    seen = set()

    for r in results:
        src = r.get("source", "UNKNOWN_SOURCE")

        if src in seen:
            continue

        seen.add(src)
        unique_sources.append({
            "source": src,
            "snippet": r.get("snippet", "")
        })


@router.post("/chat/clear")
def clear_chat():
    clear_history()
    return {"message": "Histórico limpo."}
