from fastapi import APIRouter
from app.services.search_service import semantic_search_service

router = APIRouter()


@router.post("/search")
def semantic_search(query: str):
    return semantic_search_service(query)


@router.post("/ask")
def ask_question(query: str):
    results = semantic_search_service(query)

    if not results:
        return {
            "query": query,
            "answer": "Not found in document",
            "sources": []
        }

    contexts = "\n\n".join(r["text"] for r in results)

    return {
        "query": query,
        "answer": contexts,
        "sources": [r["page"] for r in results]
    }
