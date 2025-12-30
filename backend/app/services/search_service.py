from app.config import VECTOR_STORE
from app.services.embeddings import get_embedding
import numpy as np


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def semantic_search_service(query: str, top_k: int = 3):
    query_embedding = get_embedding(query)

    results = []

    for item in VECTOR_STORE:
        score = cosine_similarity(query_embedding, item["embedding"])
        results.append({
            "text": item["text"],
            "page": item["page"],
            "score": float(score)
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]
