import math

# In-memory store (for now)
VECTOR_STORE = []

def add_chunk(chunk_id, page, text, embedding):
    VECTOR_STORE.append({
        "chunk_id": chunk_id,
        "page": page,
        "text": text,
        "embedding": embedding
    })
def cosine_similarity(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x*x for x in a))
    norm_b = math.sqrt(sum(y*y for y in b))
    return dot / (norm_a * norm_b)

def search(query_embedding, top_k=3):
    scored = []

    for item in VECTOR_STORE:
        score = cosine_similarity(query_embedding, item["embedding"])
        scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]
