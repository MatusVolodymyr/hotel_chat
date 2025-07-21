#!/usr/bin/env python3
"""
Streamlit Chat UI for Hotel Chat Application

A modern, interactive web interface for the hotel search chat bot.
"""

import streamlit as st
import sys
import os
from typing import List, Dict, Optional

# Add the project root to the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# Import modules directly to avoid circular imports
from app.core.logger import setup_logging, get_logger
from app.core.config import settings

# Initialize logging first
setup_logging(
    log_level=settings.LOG_LEVEL,
    log_file=settings.LOG_FILE,
    enable_console=False,  # Disable console logging in Streamlit
    enable_file=settings.LOG_FILE_ENABLE,
)

logger = get_logger(__name__)

# Now import the agents after logging is setup
try:
    from app.agent.lcel_agent import build_hotel_agent

    logger.info("Successfully imported agent modules")
except Exception as e:
    logger.error(f"Failed to import agent modules: {e}")
    st.error(f"Failed to import required modules: {e}")
    st.stop()


class StreamlitHotelChat:
    """Streamlit-based hotel chat interface."""

    def __init__(self):
        self._initialize_session_state()

    def _initialize_session_state(self):
        """Initialize Streamlit session state variables."""
        if "messages" not in st.session_state:
            st.session_state.messages = []

        if "agent_initialized" not in st.session_state:
            st.session_state.agent_initialized = False

        if "agent" not in st.session_state:
            st.session_state.agent = None

    def _initialize_agent(self):
        """Initialize the chat agent."""
        if not st.session_state.agent_initialized:
            try:
                logger.info("Initializing agent for Streamlit UI")

                st.session_state.agent = build_hotel_agent()
                logger.info("LCEL agent initialized for Streamlit")
                st.session_state.agent_initialized = True

            except Exception as e:
                logger.error(f"Failed to initialize agent: {e}")
                st.error(f"Failed to initialize chat agent: {e}")
                return False

        return True

    def _display_chat_history(self):
        """Display the chat history."""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def _process_user_input(self, user_input: str) -> str:
        """Process user input and get agent response."""
        logger.info(f"Processing user input in Streamlit: {user_input[:50]}...")

        try:
            if st.session_state.agent is None:
                st.error("Agent is not initialized. Please check the configuration.")
                logger.error("Attempted to invoke agent, but it is not initialized.")
                return "Agent is not initialized."

            # Convert Streamlit chat history to LangChain format
            chat_history = []
            for message in st.session_state.messages:
                content = message.get("content", "").strip()
                if content:  # Only add non-empty content
                    if message["role"] == "user":
                        chat_history.append(("human", content))
                    elif message["role"] == "assistant":
                        chat_history.append(("ai", content))

            # Keep only the last 10 exchanges (20 messages)
            if len(chat_history) > 20:
                chat_history = chat_history[-20:]

            # Debug: Log the inputs being sent to the agent
            logger.debug(f"Agent input: {user_input}")
            logger.debug(f"Chat history length: {len(chat_history)}")
            for i, (role, content) in enumerate(chat_history):
                logger.debug(f"History {i}: {role} - {content[:100]}...")

            # Invoke agent with chat history
            agent_input = {"input": user_input, "chat_history": chat_history}
            logger.debug(f"Invoking agent with: {agent_input}")

            response = st.session_state.agent.invoke(agent_input)
            result = response.get("output", str(response))
            logger.info("Response generated successfully in Streamlit")
            return result

        except Exception as e:
            logger.error(f"Error processing user input in Streamlit: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            import traceback

            logger.error(f"Full traceback: {traceback.format_exc()}")
            return f"Sorry, I encountered an error: {str(e)}"

    def _reset_conversation(self):
        """Reset the conversation history."""
        logger.info("Resetting conversation in Streamlit")
        st.session_state.messages = []

        # Reinitialize agent
        st.session_state.agent_initialized = False
        st.session_state.agent = None
        self._initialize_agent()

        st.rerun()

    def run(self):
        """Run the Streamlit chat interface."""
        # Page configuration
        st.set_page_config(
            page_title="🏨 Hotel Chat Assistant",
            page_icon="🏨",
            layout="wide",
            initial_sidebar_state="expanded",
        )

        # Sidebar
        with st.sidebar:
            st.title("🏨 Hotel Chat Settings")

            st.divider()

            # Configuration info
            st.subheader("🔧 Configuration")
            st.write(f"**Model:** {settings.LLM_MODEL}")
            st.write(f"**Temperature:** {settings.LLM_TEMPERATURE}")
            st.write(f"**Search Results:** {settings.VECTOR_SEARCH_K}")
            st.write(f"**Log Level:** {settings.LOG_LEVEL}")

            st.divider()

            # Reset button
            if st.button("🔄 Reset Conversation", use_container_width=True):
                self._reset_conversation()

            # Clear chat button
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

            st.divider()

            # Help section
            with st.expander("❓ Help & Examples"):
                st.markdown(
                    """
                **Example queries:**
                
                - "I need a luxury hotel in Kyiv"
                - "Show me budget rooms under $50"
                - "Find a family apartment with kitchen"
                - "Beach hotels in Odesa with sea view"
                - "Pet-friendly accommodation in Dnipro"
                
                **Features:**
                - Semantic search across room descriptions
                - Filter by price, location, amenities
                - Natural language understanding
                - Conversation memory
                """
                )

        # Main chat interface
        st.title("🏨 Hotel Chat Assistant")
        st.markdown("Find your perfect accommodation with AI-powered search!")

        # Check if required API keys are configured
        if settings.LLM_MODEL.startswith("gpt") and not settings.OPENAI_API_KEY:
            st.error(
                "⚠️ OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable."
            )
            st.stop()
        elif settings.LLM_MODEL.startswith("gemini") and not settings.GOOGLE_API_KEY:
            st.error(
                "⚠️ Google API key not configured. Please set the GOOGLE_API_KEY environment variable."
            )
            st.stop()

        # Initialize agent
        if not self._initialize_agent():
            st.error("Failed to initialize chat agent. Please check the logs.")
            st.stop()

        # Display chat history
        self._display_chat_history()

        # Chat input
        if prompt := st.chat_input("Ask me about hotel rooms..."):
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Searching for rooms..."):
                    response = self._process_user_input(prompt)
                st.markdown(response)

            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

        # Footer
        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; color: gray;'>"
            f"🤖 Powered by {settings.LLM_MODEL} | "
            f"🔍 Vector Search | "
            f"📊 {len(st.session_state.messages)} messages"
            "</div>",
            unsafe_allow_html=True,
        )


def main():
    """Main entry point for the Streamlit app."""
    try:
        logger.info("Starting Streamlit Hotel Chat UI")
        chat_app = StreamlitHotelChat()
        chat_app.run()
    except Exception as e:
        logger.error(f"Error in Streamlit app: {e}")
        st.error(f"Application error: {e}")


if __name__ == "__main__":
    main()
