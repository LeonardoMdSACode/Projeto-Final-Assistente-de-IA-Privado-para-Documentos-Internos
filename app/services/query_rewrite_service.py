# app/services/query_rewrite_service.py

from app.services.llm_service import ask_llm


def rewrite_query(question: str, history=None) -> str:

    history = history or []

    formatted_history = "\n".join(
        f"{m.get('role','user')}: {m.get('content','')}"
        for m in history[-6:]
    )

    prompt = f"""
Reescreve a pergunta do utilizador para uma query autónoma para RAG.

Regras:
- mantém intenção original
- resolve referências ("isso", "aquilo")
- não responder
- não inventar informação
- se histórico for irrelevante ignora

Histórico:
{formatted_history}

Pergunta:
{question}

Query:
"""

    result = ask_llm(prompt)

    return result.strip().split("\n")[0]
