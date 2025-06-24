from app.services.vector_search import search_similar_rooms
from app.db.session import get_db
from app.core.logger import get_logger
from langchain.tools import tool
from typing import Optional

logger = get_logger(__name__)


# --- Tool Wrapper ---
@tool
def search_rooms(
    query: str, location: Optional[str] = None, max_price: Optional[float] = None
) -> str:
    """
    Search hotel rooms by semantic similarity and optional filters like location and price.
    """
    logger.info(f"Room search tool called with query='{query}', location={location}, max_price={max_price}")
    
    try:
        with get_db() as db:
            logger.debug("Database session opened for room search")
            rooms = search_similar_rooms(
                db=db, query=query, location=location, max_price=max_price
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
