# chunking_service.py

import re
import nltk

nltk.data.path.append("./nltk_data")

from nltk.tokenize import sent_tokenize


def clean_text(text: str):
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def is_noise_chunk(text: str) -> bool:
    t = text.lower()

    # lixo estrutural de livro
    if "table of contents" in t:
        return True

    if t.strip().startswith("chapter"):
        return True

    # páginas de índice (muito comum em PDFs)
    if len(t.split()) < 50:
        return True

    # texto demasiado “fragmentado”
    if t.count("\n") > 20 and len(t.split()) < 80:
        return True

    # listas de páginas / headers
    if sum(c.isdigit() for c in t) > len(t) * 0.3:
        return True

    return False


def create_chunks(text: str, chunk_size=900, overlap=120):

    text = clean_text(text)
    sentences = sent_tokenize(text)

    chunks = []
    current = []
    chunk_id = 0

    def flush():
        nonlocal chunk_id, current

        if not current:
            return

        chunk_text = " ".join(current).strip()

        if is_noise_chunk(chunk_text):
            current = []
            return

        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk_text,
            "snippet": chunk_text[:300]
        })

        chunk_id += 1
        current = current[-3:]  # overlap semântico real (sentenças)

    for sentence in sentences:

        if len(sentence) > chunk_size:
            sentence = sentence[:chunk_size]

        current_text = " ".join(current + [sentence])

        if len(current_text) > chunk_size:
            flush()

        current.append(sentence)

    flush()

    return chunks
