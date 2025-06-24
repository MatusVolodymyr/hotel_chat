from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

from app.core.logger import get_logger
from app.core.config import settings

logger = get_logger(__name__)

# Load model once at module level
logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
try:
    _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    logger.info("Embedding model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load embedding model: {e}")
    raise


def embed_text(text: str) -> List[float]:
    """
    Generate a vector embedding for a given string.

    Returns a list of floats (for pgvector compatibility).
    """
    logger.debug(f"Generating embedding for text: '{text[:100]}...'")

    try:
        embedding = _model.encode(text, convert_to_numpy=True)
        embedding_list = embedding.tolist()
        logger.debug(f"Embedding generated with dimension: {len(embedding_list)}")
        return embedding_list
    except Exception as e:
        logger.error(f"Failed to generate embedding for text: {e}")
        raise


def embed_batch(texts: List[str]) -> List[List[float]]:
    """
    Batch embedding for multiple strings.
    """
    logger.info(f"Generating embeddings for batch of {len(texts)} texts")

    try:
        embeddings = _model.encode(texts, convert_to_numpy=True).tolist()
        logger.info(f"Batch embeddings generated successfully")
        return embeddings
    except Exception as e:
        logger.error(f"Failed to generate batch embeddings: {e}")
        raise
