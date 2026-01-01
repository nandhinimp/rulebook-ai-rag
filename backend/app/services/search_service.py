from app.services.chroma_store import search as chroma_search
from app.services.embeddings import get_embedding_or_mock


def semantic_search_service(query: str, top_k: int = 3):
    """Search for relevant chunks in Chroma vector store."""
    query_embedding = get_embedding_or_mock(query)
    results = chroma_search(query_embedding, top_k=top_k)
    
    # Format results for API response
    return [
        {
            "text": r["text"],
            "page": r["page"],
            "heading": r["heading"],
            "doc_id": r["doc_id"],
            "score": float(r["score"])
        }
        for r in results
    ]
