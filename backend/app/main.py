from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import pdf_upload, search

app = FastAPI(
    title="RuleBook AI",
    description="PDF-based RAG Question Answering System",
    version="1.0.0",
    swagger_ui_parameters={
        "syntaxHighlight": False,
        "tryItOutEnabled": True
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://127.0.0.1:3001", "http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pdf_upload.router)
app.include_router(search.router)

@app.get("/")
def health_check():
    return {"status": "RuleBook AI backend is running 🚀"}
