# chunking_service.py

import re
import nltk

nltk.data.path.append("./nltk_data")

from nltk.tokenize import sent_tokenize


MIN_WORDS = 80


def clean_text(text: str):

    text = text.replace("\x00", " ")

    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    # remove páginas tipo índice
    text = re.sub(r"\.{4,}\s*\d+", "", text)

    return text.strip()


def looks_like_index(text: str) -> bool:

    lines = text.splitlines()

    dotted = 0

    for line in lines:

        if re.search(r"\.{3,}\s*\d+$", line.strip()):
            dotted += 1

    return dotted >= 3


def is_noise_chunk(text: str) -> bool:

    t = text.lower().strip()

    if not t:
        return True

    # chunks demasiado pequenos
    if len(t.split()) < MIN_WORDS:
        return True

    # table of contents
    if "table of contents" in t:
        return True

    # índices remissivos
    if looks_like_index(t):
        return True

    # headers típicos
    forbidden = [
        "see also",
        "appendix",
        "index",
        "contents",
        "copyright",
        "all rights reserved",
        "isbn",
        "chapter contents"
    ]

    for f in forbidden:
        if f in t:
            return True

    # excesso de números
    digits_ratio = sum(c.isdigit() for c in t) / max(len(t), 1)

    if digits_ratio > 0.20:
        return True

    # chunk demasiado fragmentado
    if t.count("\n") > 15 and len(t.split()) < 120:
        return True

    return False


def create_chunks(text: str, chunk_size=1600, overlap_sentences=4):

    text = clean_text(text)

    sentences = sent_tokenize(text)

    chunks = []

    current = []

    chunk_id = 0

    def flush():

        nonlocal current
        nonlocal chunk_id

        if not current:
            return

        chunk_text = " ".join(current).strip()

        if is_noise_chunk(chunk_text):
            current = []
            return

        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk_text,
            "snippet": chunk_text[:350]
        })

        chunk_id += 1

        # overlap semântico
        current = current[-overlap_sentences:]

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        if len(sentence) > 1200:
            sentence = sentence[:1200]

        candidate = " ".join(current + [sentence])

        if len(candidate) > chunk_size:
            flush()

        current.append(sentence)

    flush()

    return chunks
