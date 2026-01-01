import re
from typing import List, Dict


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> List[Dict]:
    """
    Convert raw page text into meaningful chunks with overlap.
    
    Args:
        text: Raw page text
        chunk_size: Target words per chunk
        overlap: Words to overlap between chunks
    """
    # Split into sentences first
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    
    chunks = []
    current_chunk = []
    current_words = 0
    
    for sentence in sentences:
        if not sentence.strip():
            continue
            
        words = sentence.split()
        sentence_words = len(words)
        
        # Start new chunk if current is full
        if current_words + sentence_words > chunk_size and current_chunk:
            chunk_text_str = " ".join(current_chunk).strip()
            if len(chunk_text_str) > 50:  # Only keep meaningful chunks (50+ chars)
                chunks.append({
                    "text": chunk_text_str,
                    "heading": extract_heading(chunk_text_str)
                })
            
            # Keep overlap
            overlap_sentences = []
            overlap_words = 0
            for s in reversed(current_chunk):
                s_words = len(s.split())
                if overlap_words + s_words <= overlap:
                    overlap_sentences.insert(0, s)
                    overlap_words += s_words
                else:
                    break
            
            current_chunk = overlap_sentences
            current_words = overlap_words
        
        current_chunk.append(sentence)
        current_words += sentence_words
    
    # Add final chunk
    if current_chunk:
        chunk_text_str = " ".join(current_chunk).strip()
        if len(chunk_text_str) > 50:
            chunks.append({
                "text": chunk_text_str,
                "heading": extract_heading(chunk_text_str)
            })
    
    return chunks if chunks else [{"text": text, "heading": ""}]


def extract_heading(text: str) -> str:
    """Extract first line as heading if it looks like one."""
    first_line = text.split("\n")[0].strip()
    if first_line.isupper() or first_line.endswith(":"):
        return first_line.rstrip(":")
    return ""