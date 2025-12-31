from io import BytesIO

from fastapi import APIRouter, UploadFile, File, HTTPException
from pypdf import PdfReader

from app.utils.chunker import chunk_text
from app.services.embeddings import get_embedding
from app.services.store import VECTOR_STORE


router = APIRouter(prefix="/pdf", tags=["PDF"])


def extract_page_texts(data: bytes):
    """Yield (page_num, text) using pypdf only."""
    reader = PdfReader(BytesIO(data))
    for page_num, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        yield page_num, text


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    chunk_id = 0
    pages_processed = 0
    text_chunks_added = 0

    for page_num, text in extract_page_texts(data):
        pages_processed += 1
        if not text:
            continue

        chunks = chunk_text(text)
        for chunk in chunks:
            embedding = get_embedding(chunk["text"])
            VECTOR_STORE.append({
                "text": chunk["text"],
                "page": page_num,
                "chunk_id": chunk_id,
                "embedding": embedding,
                "heading": chunk.get("heading")
            })
            chunk_id += 1
            text_chunks_added += 1

    if text_chunks_added == 0:
        raise HTTPException(status_code=400, detail="No text could be extracted from the PDF. Please try a different file or a text-based PDF.")

    return {
        "filename": file.filename,
        "pages_processed": pages_processed,
        "chunks_added": text_chunks_added,
        "total_chunks": len(VECTOR_STORE),
        "sample": VECTOR_STORE[0] if VECTOR_STORE else None
    }
