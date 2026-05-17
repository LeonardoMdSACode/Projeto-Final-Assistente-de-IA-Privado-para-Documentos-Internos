# app/services/query_rewrite_service.py

from app.services.llm_service import ask_llm


def rewrite_query(question: str, history=None) -> str:

    history = history or []

    formatted_history = "\n".join(
        f"{m.get('role', 'user')}: {m.get('content', '')}"
        for m in history[-4:]
    )

    prompt = f"""
Transforma a pergunta numa query de pesquisa curta para RAG.

REGRAS:
- manter intenção original
- resolver referências contextuais
- NÃO responder
- NÃO explicar
- NÃO inventar
- output curto
- apenas uma linha

Histórico:
{formatted_history}

Pergunta:
{question}

Query:
"""

    try:

        result = ask_llm(prompt)

        result = result.strip().split("\n")[0]

        if len(result) < 3:
            return question

        return result

    except Exception:

        return question
