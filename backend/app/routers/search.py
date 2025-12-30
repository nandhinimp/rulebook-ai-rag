from fastapi import APIRouter
from app.services.search_service import semantic_search_service

router = APIRouter()


@router.post("/search")
def search(query: str):
    return semantic_search_service(query)


@router.post("/ask")
def ask(query: str):
    results = semantic_search_service(query)

    if not results:
        return {
            "query": query,
            "answer": "Not found in document",
            "sources": []
        }

    return {
        "query": query,
        "answer": "\n\n".join(r["text"] for r in results),
        "sources": [r["page"] for r in results]
    }
