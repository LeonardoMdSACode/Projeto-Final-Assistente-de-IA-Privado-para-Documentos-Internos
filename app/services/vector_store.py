# vector_store.py

import json
import numpy as np
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_PATH = BASE_DIR / "dados"

CHUNKS_FILE = DATA_PATH / "chunks.json"
VECTORS_FILE = DATA_PATH / "vectors.npy"


def save_chunks(chunks):

    with open(CHUNKS_FILE, "w", encoding="utf-8") as file:
        json.dump(chunks, file, ensure_ascii=False, indent=2)


def load_chunks():

    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_vectors(vectors):

    np.save(VECTORS_FILE, np.array(vectors))


def load_vectors():

    return np.load(VECTORS_FILE)
