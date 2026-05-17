# app\utils\similarity.py
# cosine similarity

from difflib import SequenceMatcher


def similarity(a, b):

    return SequenceMatcher(
        None,
        a,
        b
    ).ratio()


def remove_similar_chunks(
    chunks,
    threshold=0.85
):

    unique_chunks = []

    for chunk in chunks:

        is_duplicate = False

        for unique in unique_chunks:

            score = similarity(
                chunk["text"],
                unique["text"]
            )

            if score >= threshold:

                is_duplicate = True
                break

        if not is_duplicate:

            unique_chunks.append(chunk)

    return unique_chunks
