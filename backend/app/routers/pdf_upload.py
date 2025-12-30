from fastapi import APIRouter, UploadFile
from pypdf import PdfReader

from app.config import VECTOR_STORE
from app.services.embeddings import get_embedding

router = APIRouter()


def split_text(text, chunk_size=500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks


@router.post("/pdf/upload")
def upload_pdf(file: UploadFile):
    reader = PdfReader(file.file)
    chunk_id = 0

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if not text:
            continue

        chunks = split_text(text)

        for chunk in chunks:
            VECTOR_STORE.append({
                "text": chunk,
                "page": page_num,
                "chunk_id": chunk_id,
                "embedding": get_embedding(chunk)
            })
            chunk_id += 1

    return {
        "filename": file.filename,
        "total_chunks": len(VECTOR_STORE),
        "sample": VECTOR_STORE[0] if VECTOR_STORE else None
    }