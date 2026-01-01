import chromadb
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Initialize Chroma client (persistent local storage in ./chroma_data)
try:
    client = chromadb.PersistentClient(path="./chroma_data")
    
    # Delete existing collection if it has wrong dimension
    try:
        existing_collection = client.get_collection(name="rulebook_embeddings")
        client.delete_collection(name="rulebook_embeddings")
        logger.info("Deleted existing collection with incompatible dimensions")
    except:
        pass
    
    # Create new collection for embeddings
    COLLECTION = client.create_collection(
        name="rulebook_embeddings",
        metadata={"hnsw:space": "cosine"}
    )
    logger.info("Chroma persistent client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Chroma: {e}")
    raise


def upsert_chunk(doc_id: str, chunk_id: int, text: str, embedding: list, page: int, heading: Optional[str] = None):
    """
    Upsert a chunk into Chroma with metadata.
    
    Args:
        doc_id: Document ID (e.g., filename)
        chunk_id: Unique chunk ID within the document
        text: Text content of the chunk
        embedding: Embedding vector
        page: Page number
        heading: Optional section heading
    """
    try:
        COLLECTION.upsert(
            ids=[f"{doc_id}:{chunk_id}"],
            embeddings=[embedding],
            documents=[text],
            metadatas=[{
                "doc_id": doc_id,
                "chunk_id": chunk_id,
                "page": page,
                "heading": heading or ""
            }]
        )
    except Exception as e:
        logger.error(f"Failed to upsert chunk {chunk_id}: {e}")
        raise


def search(query_embedding: list, top_k: int = 3) -> list:
    """
    Search for top-k similar chunks.
    
    Returns:
        List of dicts: {text, page, heading, score, doc_id}
    """
    try:
        results = COLLECTION.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        if not results or not results["documents"] or not results["documents"][0]:
            return []
        
        output = []
        for i, (text, metadata, distance) in enumerate(
            zip(results["documents"][0], results["metadatas"][0], results["distances"][0])
        ):
            # Chroma returns distances; convert to similarity (cosine: 1 - distance)
            score = 1 - distance
            output.append({
                "text": text,
                "page": metadata.get("page"),
                "heading": metadata.get("heading", ""),
                "doc_id": metadata.get("doc_id", ""),
                "score": score
            })
        
        return output
    except Exception as e:
        logger.error(f"Failed to search: {e}")
        return []


def delete_by_doc_id(doc_id: str):
    """Delete all chunks for a document (useful for re-indexing)."""
    try:
        COLLECTION.delete(where={"doc_id": doc_id})
    except Exception as e:
        logger.error(f"Failed to delete doc {doc_id}: {e}")
