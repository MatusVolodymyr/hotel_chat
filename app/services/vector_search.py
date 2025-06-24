from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List, Optional

from app.services.embedding import embed_text
from app.models.room import Room
from app.core.logger import get_logger

logger = get_logger(__name__)


def search_similar_rooms(
    db: Session,
    query: str,
    k: int = 5,
    max_price: Optional[float] = None,
    location: Optional[str] = None,
) -> List[Room]:
    """
    Search rooms by semantic similarity + optional filters.
    """
    logger.info(
        f"Searching for rooms with query: '{query}', k={k}, max_price={max_price}, location={location}"
    )

    try:
        logger.debug("Generating query embedding")
        query_embedding = embed_text(query)
        logger.debug(
            f"Query embedding generated with dimension: {len(query_embedding)}"
        )
    except Exception as e:
        logger.error(f"Failed to generate embedding for query '{query}': {e}")
        raise

    # Raw SQL for pgvector similarity
    sql = """
    SELECT * FROM rooms
    WHERE
        (:location IS NULL OR location = :location)
        AND (:max_price IS NULL OR price <= :max_price)
    ORDER BY embedding <-> :embedding
    LIMIT :k
    """

    try:
        logger.debug("Executing vector similarity search query")
        result = db.execute(
            text(sql),
            {
                "embedding": query_embedding,
                "max_price": max_price,
                "location": location,
                "k": k,
            },
        )

        rooms = [Room(**dict(row)) for row in result]
        logger.info(f"Found {len(rooms)} matching rooms")

        if rooms:
            logger.debug(
                f"Top result: Room ID {rooms[0].id} - {rooms[0].description[:50]}..."
            )

        return rooms

    except Exception as e:
        logger.error(f"Database error during vector search: {e}")
        raise
