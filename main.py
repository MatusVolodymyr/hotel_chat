#!/usr/bin/env python3
"""
Hotel Chat Application Main Entry Point

This module provides the main entry point for the hotel chat application
with proper logging initialization and error handling.
"""

import sys
import os
from typing import Optional

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from app.core.logger import setup_logging, get_logger
from app.core.config import settings
from app.agent.lcel_agent import build_hotel_agent

# Initialize logging
setup_logging(
    log_level=settings.LOG_LEVEL,
    log_file=settings.LOG_FILE,
    enable_console=settings.LOG_CONSOLE,
    enable_file=settings.LOG_FILE_ENABLE,
)

logger = get_logger(__name__)


class HotelChatApp:
    """Main hotel chat application class."""

    def __init__(self, use_lcel: bool = True):
        """
        Initialize the hotel chat application.

        Args:
            use_lcel: Whether to use LCEL agent (True) or traditional agent (False)
        """
        logger.info("Initializing Hotel Chat Application")
        self.use_lcel = use_lcel
        self.agent = None
        self._initialize_agent()

    def _initialize_agent(self) -> None:
        """Initialize the appropriate agent type."""
        try:

            logger.info("Using LCEL-based agent")
            self.agent = build_hotel_agent()
            logger.info("Agent initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            raise

    def chat(self, user_input: str) -> str:
        """
        Process user input and return agent response.

        Args:
            user_input: User's message

        Returns:
            Agent's response
        """
        if not self.agent:
            raise RuntimeError("Agent not initialized")

        logger.info(f"Processing user message: {user_input[:50]}...")

        try:
            response = self.agent.invoke({"input": user_input})
            # LCEL agents return dict with 'output' key
            result = response.get("output", str(response))

            logger.info("Response generated successfully")
            return result

        except Exception as e:
            logger.error(f"Error processing user input: {e}")
            return f"Sorry, I encountered an error: {str(e)}"

    def reset(self) -> None:
        """Reset the agent's conversation memory."""
        logger.info("Resetting agent conversation memory")
        # For LCEL agents, we might need to reinitialize
        logger.warning("Agent doesn't have reset method, reinitializing")
        self._initialize_agent()


def interactive_chat() -> None:
    """Run an interactive chat session."""
    logger.info("Starting interactive chat session")

    try:
        app = HotelChatApp(use_lcel=True)

        print("🏨 Welcome to Hotel Chat Assistant!")
        print("Type 'quit', 'exit', or 'bye' to end the conversation.")
        print("Type 'reset' to clear conversation history.")
        print("-" * 50)

        while True:
            try:
                user_input = input("\nYou: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ["quit", "exit", "bye"]:
                    print("👋 Goodbye! Thanks for using Hotel Chat Assistant!")
                    break

                if user_input.lower() == "reset":
                    app.reset()
                    print("🔄 Conversation history cleared!")
                    continue

                response = app.chat(user_input)
                print(f"\nAssistant: {response}")

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using Hotel Chat Assistant!")
                break
            except Exception as e:
                logger.error(f"Error in interactive chat: {e}")
                print(f"❌ Sorry, an error occurred: {e}")

    except Exception as e:
        logger.error(f"Failed to start interactive chat: {e}")
        print(f"❌ Failed to start chat application: {e}")
        sys.exit(1)


def main() -> None:
    """Main entry point."""
    logger.info("Hotel Chat Application starting")

    # Check if OpenAI API key is set
    if not settings.OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY environment variable not set")
        print("❌ Please set the OPENAI_API_KEY environment variable")
        sys.exit(1)

    try:
        interactive_chat()
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)
    finally:
        logger.info("Hotel Chat Application shutting down")


if __name__ == "__main__":
    main()
