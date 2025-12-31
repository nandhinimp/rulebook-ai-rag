import re
from typing import List, Dict


def is_heading(line: str) -> bool:
    """
    Detect headings like:
    - ALL CAPS
    - Ending with :
    """
    line = line.strip()
    if not line:
        return False

    return (
        line.isupper()
        or line.endswith(":")
    )


def is_list_item(line: str) -> bool:
    """
    Detect bullet points or numbered lists
    """
    return bool(re.match(r"^(\-|\•|\d+\.)\s+", line.strip()))


def chunk_text(text: str) -> List[Dict]:
    """
    Convert raw page text into structured chunks with metadata.
    """
    lines = text.split("\n")
    chunks = []

    current_heading = None

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Heading detection
        if is_heading(line):
            current_heading = line.rstrip(":")
            chunks.append({
                "text": current_heading,
                "type": "heading",
                "heading": current_heading
            })
            continue

        # List item detection
        if is_list_item(line):
            chunks.append({
                "text": line,
                "type": "list_item",
                "heading": current_heading
            })
            continue

        # Normal paragraph
        chunks.append({
            "text": line,
            "type": "paragraph",
            "heading": current_heading
        })

    return chunks
