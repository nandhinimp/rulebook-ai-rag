import requests
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL_NAME = "nomic-embed-text"

# Load sentence-transformers model for semantic embeddings (no external service needed)
try:
    from sentence_transformers import SentenceTransformer
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    logger.info("Loaded sentence-transformers model")
except Exception as e:
    logger.warning(f"Failed to load sentence-transformers: {e}. Using mock embeddings.")
    embedding_model = None


def get_embedding(text: str, *, timeout: float = 5.0) -> list:
    """Fetch an embedding from the local Ollama server with sensible timeouts."""
    payload = {
        "model": MODEL_NAME,
        "prompt": text
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        if "embedding" not in data:
            raise HTTPException(status_code=502, detail="Embedding service response missing 'embedding' field")
        return data["embedding"]
    except requests.exceptions.Timeout as exc:
        raise HTTPException(status_code=504, detail="Embedding service timed out. Ensure Ollama is running on port 11434.") from exc
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"Embedding service error: {exc}") from exc


def get_embedding_or_mock(text: str, *, timeout: float = 5.0) -> list:
    """Get embedding using sentence-transformers (no external service)."""
    if embedding_model is not None:
        # Use sentence-transformers for semantic embeddings
        embedding = embedding_model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    else:
        # Fallback to hash-based mock
        import hashlib
        import random
        seed = int(hashlib.md5(text.encode()).hexdigest(), 16) % (2**32)
        random.seed(seed)
        embedding = [random.gauss(0, 0.1) for _ in range(384)]
        norm = sum(x**2 for x in embedding) ** 0.5
        if norm > 0:
            embedding = [x / norm for x in embedding]
        return embedding
