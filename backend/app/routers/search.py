from fastapi import APIRouter
from app.services.embeddings import get_embedding
from app.services.vector_store import search

router = APIRouter()

@router.post("/search")
def semantic_search(query: str):
    query_embedding = get_embedding(query)
    results = search(query_embedding)

    return [
        {
            "page": r["page"],
            "text": r["text"],
            "score": round(score, 3)
        }
        for score, r in results
    ]
