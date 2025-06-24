#!/usr/bin/env python3
"""
Streamlit Chat UI for Hotel Chat Application

A modern, interactive web interface for the hotel search chat bot.
"""

import streamlit as st
import sys
import os
from typing import List, Dict, Optional

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from app.core.logger import setup_logging, get_logger
from app.core.config import settings
from app.agent.lcel_agent import build_hotel_agent

# Initialize logging for Streamlit
setup_logging(
    log_level=settings.LOG_LEVEL,
    log_file=settings.LOG_FILE,
    enable_console=False,  # Disable console logging in Streamlit
    enable_file=settings.LOG_FILE_ENABLE,
)

logger = get_logger(__name__)


class StreamlitHotelChat:
    """Streamlit-based hotel chat interface."""

    def __init__(self):
        self.agent = None
        self._initialize_session_state()
        self._initialize_agent()

    def _initialize_session_state(self):
        """Initialize Streamlit session state variables."""
        if "messages" not in st.session_state:
            st.session_state.messages = []

        if "agent_initialized" not in st.session_state:
            st.session_state.agent_initialized = False

    def _initialize_agent(self):
        """Initialize the chat agent."""
        if not st.session_state.agent_initialized:
            try:
                logger.info("Initializing agent for Streamlit UI")

                self.agent = build_hotel_agent()
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
            response = self.agent.invoke({"input": user_input})
            result = response.get("output", str(response))
            logger.info("Response generated successfully in Streamlit")
            return result

        except Exception as e:
            logger.error(f"Error processing user input in Streamlit: {e}")
            return f"Sorry, I encountered an error: {str(e)}"

    def _reset_conversation(self):
        """Reset the conversation history."""
        logger.info("Resetting conversation in Streamlit")
        st.session_state.messages = []

        # Reinitialize agent
        st.session_state.agent_initialized = False
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

            # Agent type selection
            agent_type = st.radio(
                "Agent Type:",
                ["LCEL Agent", "Traditional Agent"],
                index=0 if st.session_state.use_lcel else 1,
                help="Choose between LCEL-based or traditional LangChain agent",
            )

            new_use_lcel = agent_type == "LCEL Agent"
            if new_use_lcel != st.session_state.use_lcel:
                st.session_state.use_lcel = new_use_lcel
                st.session_state.agent_initialized = False
                self._initialize_agent()
                st.rerun()

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

        # Check if OpenAI API key is configured
        if not settings.OPENAI_API_KEY:
            st.error(
                "⚠️ OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable."
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
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Searching for rooms..."):
                    response = self._process_user_input(prompt)
                st.markdown(response)

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
