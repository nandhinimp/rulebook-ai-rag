import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"

def generate_answer(query: str, contexts: list[str]) -> str:
    context_text = "\n\n".join(contexts)

    prompt = f"""
You are an AI assistant.
Answer the question ONLY using the context below.
If the answer is not present, say "Not found in document".

Context:
{context_text}

Question:
{query}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]
