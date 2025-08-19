#!/usr/bin/env python3
"""
Logging configuration for The Hero Foundry backend server.

Provides structured logging with proper formatting, log rotation, and environment-specific configuration.
"""

import logging
import logging.config
import sys
from pathlib import Path
from typing import Dict, Any

from .config import get_settings

settings = get_settings()


def setup_logging() -> None:
    """Setup logging configuration for the application."""
    
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Define logging configuration
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "json": {
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(timestamp)s %(level)s %(name)s %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG" if settings.DEBUG else "INFO",
                "formatter": "detailed" if settings.DEBUG else "default",
                "stream": sys.stdout
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "default",
                "filename": logs_dir / "hero-foundry.log",
                "maxBytes": 10 * 1024 * 1024,  # 10MB
                "backupCount": 5
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "detailed",
                "filename": logs_dir / "hero-foundry-error.log",
                "maxBytes": 10 * 1024 * 1024,  # 10MB
                "backupCount": 5
            }
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["console", "file", "error_file"],
                "level": "INFO",
                "propagate": False
            },
            "uvicorn": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False
            },
            "uvicorn.error": {
                "handlers": ["console", "file", "error_file"],
                "level": "INFO",
                "propagate": False
            },
            "uvicorn.access": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False
            },
            "sqlalchemy": {
                "handlers": ["console", "file"],
                "level": "WARNING" if not settings.DEBUG else "INFO",
                "propagate": False
            },
            "hero_foundry": {
                "handlers": ["console", "file", "error_file"],
                "level": settings.LOG_LEVEL,
                "propagate": False
            }
        }
    }
    
    # Apply logging configuration
    logging.config.dictConfig(logging_config)
    
    # Set specific logger levels based on environment
    if settings.DEBUG:
        logging.getLogger("hero_foundry").setLevel(logging.DEBUG)
        logging.getLogger("uvicorn").setLevel(logging.DEBUG)
    
    # Log startup information
    logger = logging.getLogger("hero_foundry")
    logger.info(f"Logging configured for {settings.ENVIRONMENT} environment")
    logger.info(f"Log level set to {settings.LOG_LEVEL}")
    logger.info(f"Debug mode: {settings.DEBUG}")


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the hero_foundry prefix."""
    if not name.startswith("hero_foundry"):
        name = f"hero_foundry.{name}"
    return logging.getLogger(name)


# Context manager for temporary log level changes
class TemporaryLogLevel:
    """Context manager for temporarily changing log levels."""
    
    def __init__(self, logger_name: str, level: int):
        self.logger_name = logger_name
        self.level = level
        self.original_level = None
    
    def __enter__(self):
        logger = logging.getLogger(self.logger_name)
        self.original_level = logger.level
        logger.setLevel(self.level)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.original_level is not None:
            logger = logging.getLogger(self.logger_name)
            logger.setLevel(self.original_level)


# Logging decorators
def log_function_call(logger_name: str = None):
    """Decorator to log function calls with parameters and return values."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger(logger_name or func.__module__)
            logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
            
            try:
                result = func(*args, **kwargs)
                logger.debug(f"{func.__name__} returned: {result}")
                return result
            except Exception as e:
                logger.error(f"{func.__name__} failed with error: {e}")
                raise
        
        return wrapper
    return decorator


def log_async_function_call(logger_name: str = None):
    """Decorator to log async function calls with parameters and return values."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            logger = get_logger(logger_name or func.__module__)
            logger.debug(f"Calling async {func.__name__} with args={args}, kwargs={kwargs}")
            
            try:
                result = await func(*args, **kwargs)
                logger.debug(f"Async {func.__name__} returned: {result}")
                return result
            except Exception as e:
                logger.error(f"Async {func.__name__} failed with error: {e}")
                raise
        
        return wrapper
    return decorator
