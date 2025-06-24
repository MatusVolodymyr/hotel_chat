import logging
import logging.config
import os
from typing import Optional
from datetime import datetime


class CustomFormatter(logging.Formatter):
    """Custom formatter with color support and enhanced formatting."""

    # Color codes for different log levels
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def __init__(self, fmt=None, datefmt=None, use_colors=True):
        super().__init__(fmt, datefmt)
        self.use_colors = use_colors

    def format(self, record):
        # Add module and function info
        record.module_func = f"{record.module}.{record.funcName}"

        # Add color to levelname only for console
        if self.use_colors and record.levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"
            )

        return super().format(record)


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    enable_console: bool = True,
    enable_file: bool = True,
) -> None:
    """
    Set up comprehensive logging configuration.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (defaults to logs/app.log)
        enable_console: Enable console logging
        enable_file: Enable file logging
    """
    # Create logs directory if it doesn't exist
    if log_file is None:
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = f"{log_dir}/hotel_chat_{timestamp}.log"
    else:
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

    # Define log formats
    console_format = (
        "%(asctime)s | %(levelname)s | %(module_func)s:%(lineno)d | %(message)s"
    )
    file_format = "%(asctime)s | %(levelname)s | %(name)s | %(module_func)s:%(lineno)d | %(message)s"

    # Configuration dictionary
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "()": CustomFormatter,
                "format": console_format,
                "datefmt": "%H:%M:%S",
                "use_colors": True,
            },
            "file": {
                "()": CustomFormatter,
                "format": file_format,
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "use_colors": False,
            },
        },
        "handlers": {},
        "loggers": {
            "": {  # Root logger
                "level": log_level,
                "handlers": [],
            },
            "app": {
                "level": log_level,
                "handlers": [],
                "propagate": False,
            },
            "sqlalchemy.engine": {
                "level": "WARNING",
                "handlers": [],
                "propagate": False,
            },
            "langchain": {
                "level": "WARNING",
                "handlers": [],
                "propagate": False,
            },
        },
    }

    # Add console handler if enabled
    if enable_console:
        config["handlers"]["console"] = {
            "class": "logging.StreamHandler",
            "formatter": "console",
            "level": log_level,
            "stream": "ext://sys.stdout",
        }
        config["loggers"][""]["handlers"].append("console")
        config["loggers"]["app"]["handlers"].append("console")
        config["loggers"]["sqlalchemy.engine"]["handlers"].append("console")
        config["loggers"]["langchain"]["handlers"].append("console")

    # Add file handler if enabled
    if enable_file:
        config["handlers"]["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "file",
            "level": log_level,
            "filename": log_file,
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf8",
        }
        config["loggers"][""]["handlers"].append("file")
        config["loggers"]["app"]["handlers"].append("file")
        config["loggers"]["sqlalchemy.engine"]["handlers"].append("file")
        config["loggers"]["langchain"]["handlers"].append("file")

    # Apply configuration
    logging.config.dictConfig(config)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance with the specified name.

    Args:
        name: Logger name (defaults to calling module name)

    Returns:
        Logger instance
    """
    if name is None:
        # Get the calling module name
        import inspect

        frame = inspect.currentframe()
        if frame and frame.f_back:
            name = frame.f_back.f_globals.get("__name__", "app")
        else:
            name = "app"

    return logging.getLogger(f"app.{name}")


# Convenience function to initialize logging with environment variables
def init_logging():
    """Initialize logging with settings from environment variables."""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_file = os.getenv("LOG_FILE")
    enable_console = os.getenv("LOG_CONSOLE", "true").lower() == "true"
    enable_file = os.getenv("LOG_FILE_ENABLE", "true").lower() == "true"

    setup_logging(
        log_level=log_level,
        log_file=log_file,
        enable_console=enable_console,
        enable_file=enable_file,
    )
