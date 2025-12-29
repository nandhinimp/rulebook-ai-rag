from fastapi import FastAPI
from app.routers import pdf_upload

app = FastAPI(title="RuleBook AI")

app.include_router(pdf_upload.router)

@app.get("/")
def health_check():
    return {"status": "RuleBook AI backend is running 🚀"}
