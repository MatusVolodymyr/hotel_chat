from app.services.vector_search import search_similar_rooms
from app.db.session import get_db
from app.core.logger import get_logger
from langchain.tools import tool
from typing import Optional

logger = get_logger(__name__)


# --- Alternative Tool - Semantic Only ---
@tool
def search_rooms_semantic_only(
    query: str, max_price: Optional[float] = None
) -> str:
    """
    Search hotel rooms by semantic similarity and optional price filter.
    Location filtering is handled through semantic search of descriptions.
    """
    logger.info(f"Semantic room search called with query='{query}', max_price={max_price}")
    
    try:
        with get_db() as db:
            logger.debug("Database session opened for room search")
            
            # Only use semantic search + price filter, no location filter
            rooms = search_similar_rooms(
                db=db, query=query, location=None, max_price=max_price
            )
            
            if not rooms:
                logger.info("No matching rooms found")
                return "No matching rooms found."
            
            result = "\n".join(f"[{r.location}] {r.description} - ${r.price}" for r in rooms)
            logger.info(f"Returning {len(rooms)} rooms to agent")
            logger.debug(f"Room search result: {result[:200]}...")
            return result
            
    except Exception as e:
        logger.error(f"Error in room search tool: {e}")
        return f"Error searching for rooms: {str(e)}"
