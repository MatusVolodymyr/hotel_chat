"""
Hotel Chat Application

A LangChain-based hotel room search and chat application with vector similarity search.
"""

from app.core.logger import setup_logging, get_logger, init_logging

# Initialize logging when the package is imported
init_logging()

__version__ = "1.0.0"
__author__ = "Hotel Chat Team"

# Export main functions without importing the heavy modules
__all__ = [
    "setup_logging",
    "get_logger",
    "init_logging",
]
