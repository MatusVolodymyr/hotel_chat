#!/usr/bin/env python3
"""
Hotel Chat Application Main Entry Point

This module provides the main entry point for the hotel chat application
with proper logging initialization and error handling.
"""

import sys
import os
from typing import Optional, List

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from app.core.logger import setup_logging, get_logger
from app.core.config import settings
from app.agent.lcel_agent import build_hotel_agent
from langchain_core.messages import HumanMessage, AIMessage

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

    def __init__(self):
        """Initialize the hotel chat application with LCEL agent."""
        logger.info("Initializing Hotel Chat Application")
        self.agent = None
        self.chat_history: List = []  # Store chat history as LangChain messages
        self._initialize_agent()

    def _initialize_agent(self) -> None:
        """Initialize the LCEL agent."""
        try:
            logger.info("Initializing LCEL-based agent")
            self.agent = build_hotel_agent()
            logger.info("Agent initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            raise

    def sanitize_messages_for_gemini(self, messages):
        """
        Ensure no message in the list has empty content (Gemini API limitation).
        For AI/tool-call messages (type==AIMessageChunk), fill in dummy content if missing.
        """
        patched = []
        for m in messages:
            content = getattr(m, "content", None)
            # Pydantic or BaseMessage object
            # For AIMessageChunk/tool call steps with empty content, patch it
            if hasattr(m, "additional_kwargs") and hasattr(m, "type"):
                if m.type == "ai" and content is not None and content.strip() == "":
                    # Add dummy content for Gemini
                    function_call = m.additional_kwargs.get("function_call")
                    name = (
                        function_call["name"]
                        if function_call and "name" in function_call
                        else "tool_call"
                    )
                    m.content = f"Calling tool: {name}"
            patched.append(m)
        return patched

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
        logger.debug(f"Full user input: {user_input}")
        logger.debug(f"Current chat history length: {len(self.chat_history)}")

        try:
            # Add more detailed logging for debugging
            logger.debug(f"Invoking agent with input: {user_input}")

            # Prepare the input with chat history
            sanitized_history = self.sanitize_messages_for_gemini(self.chat_history)
            agent_input = {"input": user_input, "chat_history": sanitized_history}

            response = self.agent.invoke(agent_input)
            logger.debug(f"Agent response type: {type(response)}")
            logger.debug(
                f"Agent response keys: {response.keys() if isinstance(response, dict) else 'N/A'}"
            )

            # LCEL agents return dict with 'output' key
            result = response.get("output", str(response))

            # Add this conversation to chat history
            self.chat_history.append(HumanMessage(content=user_input))
            self.chat_history.append(AIMessage(content=result))

            # Keep chat history reasonable length (last 10 exchanges = 20 messages)
            if len(self.chat_history) > 20:
                self.chat_history = self.chat_history[-20:]
                logger.debug("Trimmed chat history to last 20 messages")

            logger.info("Response generated successfully")
            logger.debug(f"Final result: {result[:100]}...")
            logger.debug(f"Updated chat history length: {len(self.chat_history)}")
            return result

        except Exception as e:
            logger.error(f"Error processing user input: {e}", exc_info=True)

            # Provide more specific error messages for common issues
            error_msg = str(e)
            if "contents.parts must not be empty" in error_msg:
                logger.error("Detected Gemini 'contents.parts must not be empty' error")
                return "Sorry, I encountered a technical issue with the AI model. This appears to be related to message formatting. Please try rephrasing your question."
            elif "rate limit" in error_msg.lower():
                return "Sorry, I'm currently receiving too many requests. Please wait a moment and try again."
            elif "api key" in error_msg.lower():
                return "Sorry, there's an issue with the AI service configuration. Please check the API key settings."
            else:
                return f"Sorry, I encountered an error: {str(e)}"

    def reset(self) -> None:
        """Reset the agent's conversation memory."""
        logger.info("Resetting agent conversation memory")
        # Clear chat history
        self.chat_history.clear()
        logger.info("Chat history cleared")

    def get_chat_history_summary(self) -> str:
        """Get a summary of the current chat history."""
        if not self.chat_history:
            return "No chat history"

        history_lines = []
        for i in range(0, len(self.chat_history), 2):
            if i + 1 < len(self.chat_history):
                human_msg = (
                    self.chat_history[i].content[:50] + "..."
                    if len(self.chat_history[i].content) > 50
                    else self.chat_history[i].content
                )
                ai_msg = (
                    self.chat_history[i + 1].content[:50] + "..."
                    if len(self.chat_history[i + 1].content) > 50
                    else self.chat_history[i + 1].content
                )
                history_lines.append(f"  {i//2 + 1}. Human: {human_msg}")
                history_lines.append(f"     AI: {ai_msg}")

        return "\n".join(history_lines)


def interactive_chat() -> None:
    """Run an interactive chat session."""
    logger.info("Starting interactive chat session")

    try:
        app = HotelChatApp()

        print("🏨 Welcome to Hotel Chat Assistant!")
        print(f"🤖 Using LLM: {settings.LLM_MODEL}")
        print("Type 'quit', 'exit', or 'bye' to end the conversation.")
        print("Type 'reset' to clear conversation history.")
        print("Type 'history' to show conversation history.")
        print("Type 'debug' to toggle debug mode.")
        print("Type 'test' to run a simple test query.")
        print("-" * 50)

        debug_mode = True

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

                if user_input.lower() == "history":
                    history = app.get_chat_history_summary()
                    print(f"\n📖 Chat History:\n{history}")
                    continue

                if user_input.lower() == "debug":
                    debug_mode = not debug_mode
                    print(f"🔧 Debug mode {'enabled' if debug_mode else 'disabled'}")
                    # Set logger level dynamically
                    if debug_mode:
                        get_logger().setLevel("DEBUG")
                    else:
                        get_logger().setLevel(settings.LOG_LEVEL)
                    continue

                if user_input.lower() == "test":
                    user_input = "I'm looking for hotels in Kyiv"
                    print(f"🧪 Running test query: {user_input}")

                if debug_mode:
                    print(f"🔧 Debug: Processing input of length {len(user_input)}")

                response = app.chat(user_input)
                print(f"\nAssistant: {response}")

                if debug_mode:
                    print(f"🔧 Debug: Response length {len(response)}")

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using Hotel Chat Assistant!")
                break
            except Exception as e:
                logger.error(f"Error in interactive chat: {e}", exc_info=True)
                print(f"❌ Sorry, an error occurred: {e}")

    except Exception as e:
        logger.error(f"Failed to start interactive chat: {e}", exc_info=True)
        print(f"❌ Failed to start chat application: {e}")
        sys.exit(1)


def main() -> None:
    """Main entry point."""
    logger.info("Hotel Chat Application starting")

    # Check API keys based on configured LLM model
    logger.info(f"Configured LLM model: {settings.LLM_MODEL}")

    if settings.LLM_MODEL.startswith("gpt"):
        if not settings.OPENAI_API_KEY:
            logger.error("OPENAI_API_KEY environment variable not set")
            print(
                "❌ Please set the OPENAI_API_KEY environment variable for OpenAI models"
            )
            sys.exit(1)
        logger.info("Using OpenAI LLM")
    elif settings.LLM_MODEL.startswith("gemini"):
        if not settings.GOOGLE_API_KEY:
            logger.error("GOOGLE_API_KEY environment variable not set")
            print(
                "❌ Please set the GOOGLE_API_KEY environment variable for Gemini models"
            )
            sys.exit(1)
        logger.info("Using Google Gemini LLM")
    else:
        logger.error(f"Unsupported LLM model: {settings.LLM_MODEL}")
        print(f"❌ Unsupported LLM model: {settings.LLM_MODEL}")
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
