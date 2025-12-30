from fastapi import APIRouter, UploadFile, File, HTTPException
from pypdf import PdfReader
from app.utils.chunker import chunk_text
from app.services.embedding_pipeline import embed_chunks

router = APIRouter(prefix="/pdf", tags=["PDF"])

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    reader = PdfReader(file.file)
    all_chunks = []

    for page_index, page in enumerate(reader.pages):
        page_text = page.extract_text()

        if not page_text:
            continue

        page_chunks = chunk_text(page_text)

        for chunk in page_chunks:
            all_chunks.append({
                "page": page_index + 1,
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"]
            })

    embedded_chunks = embed_chunks(all_chunks)

    return {
        "filename": file.filename,
        "total_chunks": len(embedded_chunks),
        "sample": {
            "page": embedded_chunks[0]["page"],
            "chunk_id": embedded_chunks[0]["chunk_id"],
            "embedding_dim": len(embedded_chunks[0]["embedding"])
        }
    }
