from fastapi import APIRouter
from app.services.search_service import semantic_search_service

router = APIRouter()


@router.post("/search")
def semantic_search(query: str):
    """Search for relevant chunks across all uploaded PDFs."""
    results = semantic_search_service(query)
    return {
        "query": query,
        "results": results,
        "count": len(results)
    }


@router.post("/ask")
def ask_question(query: str):
    """Ask a question and get an answer with citations from PDFs."""
    results = semantic_search_service(query, top_k=5)  # Get top 5, then filter strictly

    if not results:
        return {
            "query": query,
            "answer": "Information not found in uploaded documents",
            "sources": []
        }

    # Return only the BEST matching chunk (highest relevance score)
    if results:
        top_result = results[0]  # Only the best match
        answer = top_result["text"]
        sources = [{
            "document": top_result["doc_id"],
            "page": top_result["page"],
            "heading": top_result["heading"],
            "score": round(top_result["score"], 3)
        }]

        return {
            "query": query,
            "answer": answer,
            "sources": sources
        }
    
    return {
        "query": query,
        "answer": "No matching information found for this query",
        "sources": []
    }
