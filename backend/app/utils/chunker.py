def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50):
    words = text.split()
    chunks = []

    start = 0
    chunk_id = 1

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]

        chunks.append({
            "chunk_id": chunk_id,
            "text": " ".join(chunk_words)
        })

        chunk_id += 1
        start = end - overlap

    return chunks
