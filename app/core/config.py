import os
from typing import Optional
from dotenv import load_dotenv

# Load .env file into environment
load_dotenv()


class Settings:
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost/hotel_db"
    )

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/hotel_chat.log")
    LOG_CONSOLE: bool = os.getenv("LOG_CONSOLE", "true").lower() == "true"
    LOG_FILE_ENABLE: bool = os.getenv("LOG_FILE_ENABLE", "true").lower() == "true"

    # OpenAI
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")

    # Model settings
    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )

    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-2.0-flash")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0"))

    # Vector search configuration
    VECTOR_SEARCH_K: int = int(os.getenv("VECTOR_SEARCH_K", "5"))

    # Agent configuration
    AGENT_VERBOSE: bool = os.getenv("AGENT_VERBOSE", "false").lower() == "true"


settings = Settings()
