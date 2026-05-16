# app\services\router_service.py

from app.services.llm_service import ask_llm


def decide(question: str, history=None):

    # MEMORY fallback trigger (só comportamento)
    memory_triggers = [
        "isso", "esse", "explica melhor",
        "o que foi dito", "anterior"
    ]

    q = question.lower()

    if any(t in q for t in memory_triggers):
        return "MEMORY_HINT"

    return "RAG"
