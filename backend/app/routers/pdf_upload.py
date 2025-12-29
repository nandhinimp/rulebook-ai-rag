from fastapi import APIRouter, UploadFile, File, HTTPException
from pypdf import PdfReader

router = APIRouter(prefix="/pdf", tags=["PDF"])

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    try:
        reader = PdfReader(file.file)
        text = ""

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

        return {
            "filename": file.filename,
            "pages": len(reader.pages),
            "text_length": len(text)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
