# app/services/query_rewrite_service.py

import re


def rewrite_query(question: str, history=None) -> str:

    original = question.strip()

    rewritten = original.lower()

    # remove padrões fracos de pergunta
    patterns = [
        "o que encontras sobre",
        "o que me podes dizer sobre",
        "fala sobre",
        "explica",
        "qual é",
    ]

    for p in patterns:
        rewritten = rewritten.replace(p, "")

    rewritten = re.sub(r"[^\w\sà-ÿ]", " ", rewritten)
    rewritten = re.sub(r"\s+", " ", rewritten).strip()

    # 🔧 DEBUG OUTPUT
    print("\n[QUERY ORIGINAL]")
    print(original)

    print("\n[QUERY REWRITTEN]")
    print(rewritten)

    return rewritten if len(rewritten) > 2 else original