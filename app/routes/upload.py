# upload.py
# upload de documentos

import os
from fastapi import APIRouter, UploadFile, File
import shutil
from pathlib import Path

from indexar import run_indexing_pipeline

router = APIRouter()

os.makedirs("data/documents", exist_ok=True)
UPLOAD_FOLDER = Path("data/documents")


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    
    print("UPLOAD RECEBIDO")
    
    filename = file.filename.lower()
    
    print(filename)

    if not (
        filename.endswith(".pdf")
        or filename.endswith(".txt")
    ):
        return {
            "error": "Formato inválido"
        }

    save_path = UPLOAD_FOLDER / file.filename

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    run_indexing_pipeline()

    return {
        "message": "Documento carregado com sucesso"
    }
