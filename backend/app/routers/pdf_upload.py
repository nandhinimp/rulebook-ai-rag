from fastapi import APIRouter, UploadFile, File, HTTPException
from pypdf import PdfReader

from app.utils.chunker import chunk_text
from app.services.embeddings import get_embedding
from app.services.store import VECTOR_STORE


router = APIRouter(prefix="/pdf", tags=["PDF"])


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    reader = PdfReader(file.file)
    chunk_id = 0

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if not text:
            continue

        chunks = chunk_text(text)

        for chunk in chunks:
            embedding = get_embedding(chunk["text"])

            VECTOR_STORE.append({
                "text": chunk["text"],
                "page": page_num,
                "chunk_id": chunk_id,
                "embedding": embedding
            })

            chunk_id += 1

    return {
        "filename": file.filename,
        "total_chunks": len(VECTOR_STORE),
        "sample": VECTOR_STORE[0] if VECTOR_STORE else None
    }
