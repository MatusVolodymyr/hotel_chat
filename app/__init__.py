"""
Hotel Chat Application

A LangChain-based hotel room search and chat application with vector similarity search.
"""

from app.core.logger import setup_logging, get_logger, init_logging

# Initialize logging when the package is imported
init_logging()

__version__ = "1.0.0"
__author__ = "Me"

# Make key components easily importable
from app.agent.lcel_agent import build_hotel_agent
from app.services.vector_search import search_similar_rooms
from app.models.room import Room

__all__ = [
    "build_hotel_agent",
    "search_similar_rooms",
    "Room",
    "setup_logging",
    "get_logger",
]
