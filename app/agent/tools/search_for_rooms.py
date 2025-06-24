from app.services.vector_search import search_similar_rooms
from app.db.session import get_db
from app.core.logger import get_logger
from langchain.tools import tool
from typing import Optional
from difflib import get_close_matches
from sqlalchemy import text

logger = get_logger(__name__)


def normalize_location(location: Optional[str], db) -> Optional[str]:
    """
    Normalize location using fuzzy matching against existing locations in database.
    """
    if not location:
        return None

    # Get all unique locations from database
    result = db.execute(text("SELECT DISTINCT location FROM rooms"))
    db_locations = [row[0] for row in result]

    # Try exact match first (case insensitive)
    for db_loc in db_locations:
        if location.lower() == db_loc.lower():
            logger.debug(f"Exact location match: '{location}' -> '{db_loc}'")
            return db_loc

    # Try fuzzy matching
    matches = get_close_matches(
        location.lower(), [loc.lower() for loc in db_locations], n=1, cutoff=0.6
    )
    if matches:
        # Find the original case version
        for db_loc in db_locations:
            if db_loc.lower() == matches[0]:
                logger.info(f"Fuzzy location match: '{location}' -> '{db_loc}'")
                return db_loc

    # If no match found, return None to search all locations
    logger.info(f"No location match found for '{location}', searching all locations")
    return None


# --- Tool Wrapper ---
@tool
def search_rooms(
    query: str, location: Optional[str] = None, max_price: Optional[float] = None
) -> str:
    """
    Search hotel rooms by semantic similarity and optional filters.

    Args:
        query: Natural language description of what the user is looking for
        location: Exact location name if specified (e.g., "Kyiv", "Odesa", "Carpathian Mountains").
                 Leave None if unsure about exact name - semantic search will handle location matching.
        max_price: Maximum price per night in USD

    Note: If location matching fails, the search will include all locations and rely on semantic similarity.
    """
    logger.info(
        f"Room search tool called with query='{query}', location={location}, max_price={max_price}"
    )

    try:
        with get_db() as db:
            logger.debug("Database session opened for room search")

            # Normalize location if provided
            normalized_location = normalize_location(location, db)

            rooms = search_similar_rooms(
                db=db, query=query, location=normalized_location, max_price=max_price
            )

            if not rooms:
                logger.info("No matching rooms found")
                return "No matching rooms found."

            result = "\n".join(
                f"[{r.location}] {r.description} - ${r.price}" for r in rooms
            )
            logger.info(f"Returning {len(rooms)} rooms to agent")
            logger.debug(f"Room search result: {result[:200]}...")
            
            # Ensure we never return an empty string
            return result if result.strip() else "No matching rooms found."

    except Exception as e:
        logger.error(f"Error in room search tool: {e}")
        return f"Error searching for rooms: {str(e)}"
