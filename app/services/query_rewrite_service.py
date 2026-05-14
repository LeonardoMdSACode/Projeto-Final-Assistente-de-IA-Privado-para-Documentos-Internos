# app/services/query_rewrite_service.py

from app.services.llm_service import ask_llm
from app.services.memory_service import get_history


def rewrite_query(question: str) -> str:

    history = get_history()

    formatted_history = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in history[-6:]
    )

    prompt = f"""
Tu és um sistema de reescrita de queries para um sistema RAG.

Tarefa:
- Reescreve a pergunta do utilizador para uma query autónoma
- Expande referências vagas (ex: "isso", "esse tópico")
- Mantém apenas intenção de pesquisa
- Não respondas à pergunta

Histórico:
{formatted_history}

Pergunta:
{question}

Responde apenas com a query reescrita:
"""

    rewritten = ask_llm(prompt).strip().split("\n")[0]

    return rewritten.strip()
