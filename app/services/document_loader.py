# document_loader.py
# leitura TXT/PDF

import os
from pypdf import PdfReader


DOCUMENTS_PATH = "data/documents"


def load_all_documents():

    documents = []

    for filename in os.listdir(DOCUMENTS_PATH):

        filepath = os.path.join(
            DOCUMENTS_PATH,
            filename
        )

        text = ""

        # TXT
        if filename.endswith(".txt"):

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                text = file.read()

        # PDF
        elif filename.endswith(".pdf"):

            reader = PdfReader(filepath)

            for page in reader.pages:
                extracted = page.extract_text()

                if extracted:
                    cleaned = extracted.replace("\x00", " ")

                    text += cleaned + "\n"

        if text.strip():

            documents.append({
                "text": text,
                "source": filename
            })

    return documents
