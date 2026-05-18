# app/services/retrieval_service.py

from app.services.embedding_service import generate_embedding
from app.services.vector_store import search_chunks
from app.services.reranker_service import rerank
import re   # 🔧 ADICIONADO

MIN_SCORE = -0.5


# 🔧 NOVO: normalização consistente (mínima, genérica)
def tokenize(text: str):
    text = text.lower()

    # normalização de underscores
    text = text.replace("_", " ")

    text = re.sub(r"[^\w\s]", " ", text)
    return [t for t in text.split() if len(t) > 1]


def deduplicate_chunks(results):

    seen = set()
    final = []

    for r in results:

        text = r["text"][:300].lower()

        if text in seen:
            continue

        seen.add(text)

        final.append(r)

    return final


def search(query, history=None):

    query_embedding = generate_embedding(query)

    results = search_chunks(
        query_embedding,
        top_k=20
    )

    # 🔧 FIX 1: tokenização consistente
    query_terms = tokenize(query.replace("_", " "))

    lexical_filtered = []

    for r in results:

        text = r["text"].lower()

        # 🔧 FIX 2: tokenização do texto também (resolve bootstrap_css vs bootstrap css)
        text_tokens = tokenize(text)

        match_score = sum(term in text_tokens for term in query_terms)

        if match_score > 0:
            r["lexical_score"] = match_score
            lexical_filtered.append(r)

    # só usa fallback se existir match lexical
    if lexical_filtered:
        results = sorted(
            lexical_filtered + results[:5],
            key=lambda x: x.get("lexical_score", 0),
            reverse=True
        )

    if not results:
        return []

    results = deduplicate_chunks(results)

    ranked = rerank(
        query,
        results,
        top_k=9
    )

    # 🔧 FIX 3: keywords mais limpas (evita lixo tipo "o", "de", etc)
    query_terms = [t for t in tokenize(query) if len(t) > 2]

    filtered = []

    for r in ranked:

        score = r.get("score", 0)

        score_bonus = 0

        # agora consistente com tokens do texto
        text_tokens = tokenize(r["text"])

        for term in query_terms:
            if term in text_tokens:
                score_bonus += 1

        r["keyword_score"] = score_bonus

        if score >= MIN_SCORE:
            filtered.append(r)

    # ordenação final híbrida (ligeiramente mais robusta)
    filtered = sorted(
        filtered,
        key=lambda x: (
            x.get("score", 0) * 2 +   # embedding pesa mais
            x.get("keyword_score", 0) +
            x.get("lexical_score", 0)
        ),
        reverse=True
    )

    return filtered


def keyword_filter(query, results):
    q = query.lower().replace("{", "").replace("}", "")
    q_terms = set(tokenize(q))

    filtered = []

    for r in results:
        text = tokenize(r["text"])

        if any(term in text for term in q_terms):
            filtered.append(r)

    return filtered or results
