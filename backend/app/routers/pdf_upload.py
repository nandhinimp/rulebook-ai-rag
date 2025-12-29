from fastapi import APIRouter, UploadFile, File, HTTPException
from pypdf import PdfReader  # type: ignore
from app.utils.chunker import chunk_text

router = APIRouter(prefix="/pdf", tags=["PDF"])

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    reader = PdfReader(file.file)
    full_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    chunks = chunk_text(full_text)

    return {
        "filename": file.filename,
        "pages": len(reader.pages),
        "total_chunks": len(chunks),
        "sample_chunk": chunks[0][:300]  # preview
    }
