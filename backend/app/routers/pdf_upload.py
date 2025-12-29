from fastapi import APIRouter, UploadFile, File, HTTPException
from pypdf import PdfReader
from app.utils.chunker import chunk_text

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

    return {
        "filename": file.filename,
        "pages": len(reader.pages),
        "total_chunks": len(all_chunks),
        "sample_chunk": all_chunks[0]
    }
