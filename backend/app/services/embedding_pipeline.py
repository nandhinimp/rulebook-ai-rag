from app.services.embeddings import get_embedding

def embed_chunks(chunks: list[dict]):
    """
    Input:
      [
        { "page": 1, "chunk_id": 1, "text": "..." },
        ...
      ]

    Output:
      [
        {
          "page": 1,
          "chunk_id": 1,
          "text": "...",
          "embedding": [768 floats]
        }
      ]
    """
    embedded_chunks = []

    for chunk in chunks:
        vector = get_embedding(chunk["text"])

        embedded_chunks.append({
            "page": chunk["page"],
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            "embedding": vector
        })

    return embedded_chunks
