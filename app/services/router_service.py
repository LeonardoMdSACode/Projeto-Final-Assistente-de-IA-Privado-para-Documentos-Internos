# app\services\router_service.py

from app.services.llm_service import ask_llm


def decide(question: str, history=None):

    # MEMORY fallback trigger (só comportamento)
    memory_triggers = [
        "isso",
        "esse",
        "essa",
        "anterior",
        "antes",
        "primeira conversa",
        "primeiro assunto",
        "o que disseste",
        "o que falamos",
        "lembras",
        "falámos",
        "falamos",
        "conversa anterior",
        "histórico"
    ]

    q = question.lower()

    if any(t in q for t in memory_triggers):
        return "MEMORY_HINT"

    return "RAG"
