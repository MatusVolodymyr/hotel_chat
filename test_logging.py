#!/usr/bin/env python3
"""
Test script to verify logging configuration and basic functionality.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from app.core.logger import setup_logging, get_logger
from app.core.config import settings


def test_logging():
    """Test different logging levels and functionality."""

    # Initialize logging
    setup_logging(log_level="DEBUG", enable_console=True, enable_file=True)

    logger = get_logger("test")

    print("🧪 Testing logging functionality...")
    print("-" * 40)

    # Test different log levels
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    logger.critical("This is a CRITICAL message")

    # Test structured logging
    logger.info(
        "Testing structured logging",
        extra={
            "user_id": "12345",
            "action": "room_search",
            "query": "luxury hotel in Kyiv",
        },
    )

    # Test exception logging
    try:
        raise ValueError("This is a test exception")
    except Exception as e:
        logger.exception("Caught an exception during testing")

    # Test configuration access
    logger.info(f"Current log level: {settings.LOG_LEVEL}")
    logger.info(f"Database URL configured: {bool(settings.DATABASE_URL)}")
    logger.info(f"OpenAI API key configured: {bool(settings.OPENAI_API_KEY)}")

    print("\n✅ Logging test completed!")
    print(f"📁 Log file location: {settings.LOG_FILE}")


def test_imports():
    """Test that all main modules can be imported."""

    logger = get_logger("import_test")
    logger.info("Testing module imports...")

    try:
        from app.models.room import Room

        logger.info("✅ Room model imported successfully")
    except Exception as e:
        logger.error(f"❌ Failed to import Room model: {e}")

    try:
        from app.services.embedding import embed_text

        logger.info("✅ Embedding service imported successfully")
    except Exception as e:
        logger.error(f"❌ Failed to import embedding service: {e}")

    try:
        from app.services.vector_search import search_similar_rooms

        logger.info("✅ Vector search service imported successfully")
    except Exception as e:
        logger.error(f"❌ Failed to import vector search service: {e}")

    try:
        from app.agent.hotel_agent import HotelSearchAgent

        logger.info("✅ Hotel agent imported successfully")
    except Exception as e:
        logger.error(f"❌ Failed to import hotel agent: {e}")

    try:
        from app.agent.lcel_agent import build_hotel_agent

        logger.info("✅ LCEL agent imported successfully")
    except Exception as e:
        logger.error(f"❌ Failed to import LCEL agent: {e}")

    try:
        from app.agent.tools.search_for_rooms import search_rooms

        logger.info("✅ Search rooms tool imported successfully")
    except Exception as e:
        logger.error(f"❌ Failed to import search rooms tool: {e}")


if __name__ == "__main__":
    print("🏨 Hotel Chat - Logging Test")
    print("=" * 40)

    test_logging()
    print()
    test_imports()

    print("\n🎉 All tests completed!")
