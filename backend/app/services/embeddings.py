import requests
from fastapi import HTTPException

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL_NAME = "nomic-embed-text"


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
