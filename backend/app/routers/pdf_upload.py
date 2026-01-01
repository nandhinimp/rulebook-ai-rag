from io import BytesIO
import logging
import asyncio

from fastapi import APIRouter, UploadFile, File, HTTPException
from pypdf import PdfReader

from app.utils.chunker import chunk_text
from app.services.embeddings import get_embedding_or_mock
from app.services.chroma_store import upsert_chunk

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/pdf", tags=["PDF"])


def extract_page_texts(data: bytes):
    """Yield (page_num, text) using pypdf only."""
    reader = PdfReader(BytesIO(data))
    for page_num, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        yield page_num, text


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files allowed")

        data = await file.read()
        if not data:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        chunk_id = 0
        pages_processed = 0
        text_chunks_added = 0
        doc_id = file.filename

        logger.info(f"Starting upload for {doc_id}")

        for page_num, text in extract_page_texts(data):
            pages_processed += 1
            if not text:
                continue

            chunks = chunk_text(text)
            for chunk in chunks:
                try:
                    # Get embedding with fallback
                    embedding = get_embedding_or_mock(chunk["text"])
                    
                    # Upsert to Chroma
                    upsert_chunk(
                        doc_id=doc_id,
                        chunk_id=chunk_id,
                        text=chunk["text"],
                        embedding=embedding,
                        page=page_num,
                        heading=chunk.get("heading")
                    )
                    chunk_id += 1
                    text_chunks_added += 1
                except Exception as chunk_err:
                    logger.warning(f"Skipping chunk {chunk_id}: {chunk_err}")
                    chunk_id += 1
                    continue

        if text_chunks_added == 0:
            raise HTTPException(status_code=400, detail="No text could be extracted from the PDF.")

        logger.info(f"Upload complete: {text_chunks_added} chunks indexed")
        return {
            "filename": file.filename,
            "doc_id": doc_id,
            "pages_processed": pages_processed,
            "chunks_added": text_chunks_added,
            "message": f"Successfully indexed {text_chunks_added} chunks"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
