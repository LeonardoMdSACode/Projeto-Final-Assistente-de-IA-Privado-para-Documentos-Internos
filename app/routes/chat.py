# app/routes/chat.py

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.retrieval_service import search
from app.services.llm_service import ask_llm
from app.services.memory_service import add_message, get_history, clear_history
from app.services.vector_store import collection
from app.services.query_rewrite_service import rewrite_query

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


def is_greeting(q: str) -> bool:
    q = q.lower().strip()
    return any(k in q for k in [
        "olá", "ola", "hello", "hi",
        "bom dia", "boa tarde", "boa noite"
    ])


def is_doc_list_query(q: str) -> bool:
    q = q.lower()
    return any(k in q for k in [
        "que documentos",
        "quais documentos",
        "lista de documentos",
        "que ficheiros",
        "quais livros",
        "que livros"
    ])


def format_sources(results):

    seen = set()
    sources = []

    for r in results:
        src = r.get("source", "UNKNOWN_SOURCE")

        if src in seen:
            continue

        seen.add(src)
        sources.append(src)

    return sources[:2]


def format_excerpts(results, max_items=2):

    seen = set()
    excerpts = []

    for r in results:

        text = r.get("text", "").strip()
        if not text:
            continue

        # 🔥 chave MAIS forte (evita duplicação real)
        key = (r.get("source"), r.get("chunk_id"))

        if key in seen:
            continue

        seen.add(key)

        excerpts.append({
            "source": r.get("source"),
            "chunk_id": r.get("chunk_id"),
            "text": text[:450]
        })

        if len(excerpts) >= max_items:
            break

    return excerpts


@router.post("/chat")
def chat(request: ChatRequest):

    question = request.question.strip()
    add_message("user", question)

    history = get_history()

    results = []
    answer = ""

    # ---------------- GREETING ----------------
    if is_greeting(question):
        answer = "Olá. Como posso ajudar?"

        add_message("assistant", answer)

        return {
            "answer": answer,
            "sources": [],
            "chunks": []
        }

    # ---------------- DOC LIST ----------------
    elif is_doc_list_query(question):

        docs = collection.get(include=["metadatas"])

        unique_docs = sorted(set(
            m.get("source", "UNKNOWN_SOURCE")
            for m in docs.get("metadatas", [])
        ))

        answer = "Documentos na base de dados:\n\n" + "\n".join(unique_docs)
        
        add_message("assistant", answer)

        return {
            "answer": answer,
            "sources": [],
            "chunks": []
        }

    # ---------------- RAG ----------------
    else:

        rewritten_query = rewrite_query(question, history=history)

        results = search(rewritten_query, history=history)

        if not results:
            answer = "Não encontrei essa informação nos documentos."

            add_message("assistant", answer)

            return {
                "answer": answer,
                "sources": [],
                "chunks": []
            }

        # 🔥 TUDO LOCALIZADO AQUI (NUNCA SAI DO BLOCO)

        context = "\n\n".join(r["text"] for r in results)

        formatted_history = "\n".join(
            f"{m['role']}: {m['content']}"
            for m in history[-6:]
        )

        prompt = f"""
Tu és um assistente que responde usando documentos recuperados por RAG.

IMPORTANTE:
- Só podes usar informação explicitamente presente nos DOCUMENTOS
- Resume e sintetiza a informação encontrada
- Se não estiver nos documentos, diz "Não encontrei essa informação."
- Só dizer "Não encontrei essa informação."
  se o contexto estiver realmente vazio ou irrelevante
- NÃO inventes informação fora dos documentos
- Não generalizes conhecimento

HISTÓRICO:
{formatted_history}

DOCUMENTOS:
{context}

PERGUNTA:
{question}
"""

        answer = ask_llm(prompt)
        unique_sources = list(dict.fromkeys(
            r["source"] for r in results
        ))[:2]
        unique_excerpts = []
        seen = set()
        for r in results:
            key = (r["source"], r["chunk_id"])
            if key in seen:
                continue
            
            seen.add(key)
            unique_excerpts.append({
                "source": r["source"],
                "chunk_id": r["chunk_id"],
                "text": r["text"][:400]
            })
            if len(unique_excerpts) >= 2:
                break

    # FINAL OUTPUT (ÚNICO LOCAL DE FORMATAÇÃO)

    answer += "\n\nFontes:\n"
    answer += "\n".join(f"- {s}" for s in unique_sources)
    answer += "\n\nExcertos:\n\n"
    for e in unique_excerpts:
        answer += (
            "━━━━━━━━━━━━━━━━━━\n"
            f"SOURCE: {e['source']}\n"
            f"CHUNK: {e['chunk_id']}\n\n"
            f"{e['text']}\n\n"
        )

    add_message("assistant", answer)

    return {
            "answer": answer,
            "sources": unique_sources,
            "chunks": unique_excerpts
        }


@router.post("/chat/clear")
def clear_chat():
    clear_history()
    return {"message": "Histórico limpo."}


@router.post("/clear")
def clear_chat_legacy():
    clear_history()
    return {"message": "Histórico limpo."}
