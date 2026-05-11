# document_loader.py
# leitura TXT/PDF

from pathlib import Path
import fitz


BASE_DIR = Path(__file__).resolve().parent.parent.parent

DOCUMENTS_PATH = BASE_DIR / "documentos"


def load_txt(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def load_pdf(file_path):

    document = fitz.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


def load_all_documents():

    documents = []

    for file_path in DOCUMENTS_PATH.iterdir():

        if file_path.suffix == ".txt":
            text = load_txt(file_path)

        elif file_path.suffix == ".pdf":
            text = load_pdf(file_path)

        else:
            continue

        documents.append({
            "filename": file_path.name,
            "text": text
        })

    return documents
