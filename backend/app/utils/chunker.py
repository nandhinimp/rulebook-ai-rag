def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)
        chunks.append(chunk_text)

        start = end - overlap  # move with overlap

    return chunks
