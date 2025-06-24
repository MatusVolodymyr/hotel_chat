from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from app.core.logger import get_logger
from contextlib import contextmanager
from typing import Generator

logger = get_logger(__name__)

# Engine: the core connection to PostgreSQL
logger.info("Initializing database engine")
engine = create_engine(settings.DATABASE_URL, echo=False)
logger.info("Database engine created successfully")

# Session factory: create new sessions when needed
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Dependency-style DB session generator.
    Ensures commit/rollback and close.
    """
    logger.debug("Creating new database session")
    db = SessionLocal()
    try:
        yield db
        db.commit()
        logger.debug("Database session committed successfully")
    except Exception as e:
        logger.error(f"Database session error, rolling back: {e}")
        db.rollback()
        raise
    finally:
        db.close()
        logger.debug("Database session closed")
