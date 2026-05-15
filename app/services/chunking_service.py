# chunking_service.py


def create_chunks(text, chunk_size=800, overlap=200):

    chunks = []
    start = 0
    chunk_id = 0

    while start < len(text):

        end = start + chunk_size
        chunk = text[start:end]

        chunks.append({
            "text": chunk,
            "chunk_id": chunk_id,
            "start": start,
            "end": end,
            "snippet": chunk[:200]  # NÍVEL 1 — excerto rápido
        })

        start += chunk_size - overlap
        chunk_id += 1

    return chunks
