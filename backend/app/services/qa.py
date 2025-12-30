def build_prompt(query: str, chunks: list[str]) -> str:
    context = "\n\n".join(chunks)

    return f"""
You are a document assistant.

Answer the question using ONLY the information provided below.
If the answer is not explicitly present, say:
"Not found in document."

Context:
{context}

Question:
{query}

Answer:
""".strip()
