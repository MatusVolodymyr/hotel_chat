import os
from typing import Optional
from dotenv import load_dotenv

# Load .env file into environment
load_dotenv()


class Settings:
    # Database
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "hotel_chat")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))

    DATABASE_URL: str = os.getenv("DATABASE_URL") or (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
        f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
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
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4.1-nano")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0"))

    # Vector search configuration
    VECTOR_SEARCH_K: int = int(os.getenv("VECTOR_SEARCH_K", "3"))

    # Agent configuration
    AGENT_VERBOSE: bool = os.getenv("AGENT_VERBOSE", "false").lower() == "true"

    model_config = {"env_file": ".env"}


settings = Settings()
