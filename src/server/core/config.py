#!/usr/bin/env python3
"""
Configuration management for The Hero Foundry backend server.

Handles environment variables, application settings, and configuration validation.
"""

import os
from functools import lru_cache
from typing import List, Optional
from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application settings
    APP_NAME: str = "The Hero Foundry"
    APP_VERSION: str = "2.0.0"
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Server settings
    HOST: str = Field(default="127.0.0.1", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    
    # CORS and security
    ALLOWED_HOSTS: List[str] = Field(
        default=["http://localhost:1420", "http://127.0.0.1:1420"],
        env="ALLOWED_HOSTS"
    )
    
    # Database settings
    DATABASE_URL: str = Field(
        default="postgresql://hero_foundry:password@localhost:5432/hero_foundry",
        env="DATABASE_URL"
    )
    DATABASE_POOL_SIZE: int = Field(default=10, env="DATABASE_POOL_SIZE")
    DATABASE_MAX_OVERFLOW: int = Field(default=20, env="DATABASE_MAX_OVERFLOW")
    
    # Redis settings
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        env="REDIS_URL"
    )
    REDIS_POOL_SIZE: int = Field(default=10, env="REDIS_POOL_SIZE")
    
    # AI and external services
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4o-mini", env="OPENAI_MODEL")
    
    # File storage
    STORAGE_PATH: str = Field(
        default="./storage",
        env="STORAGE_PATH"
    )
    MAX_FILE_SIZE: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    
    # Ruleset settings
    RULESET_PATH: str = Field(
        default="./content/rulesets",
        env="RULESET_PATH"
    )
    DEFAULT_RULESET: str = Field(default="dnd5e", env="DEFAULT_RULESET")
    
    # Character export settings
    EXPORT_PATH: str = Field(
        default="./exports",
        env="EXPORT_PATH"
    )
    EXPORT_FORMATS: List[str] = Field(
        default=["pdf", "png", "json"],
        env="EXPORT_FORMATS"
    )
    
    # Validation settings
    MAX_CHARACTERS_PER_USER: int = Field(default=100, env="MAX_CHARACTERS_PER_USER")
    MAX_HOMEBREW_ITEMS: int = Field(default=1000, env="MAX_HOMEBREW_ITEMS")
    
    @validator("ALLOWED_HOSTS", pre=True)
    def parse_allowed_hosts(cls, v):
        """Parse ALLOWED_HOSTS from comma-separated string or list."""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v
    
    @validator("EXPORT_FORMATS", pre=True)
    def parse_export_formats(cls, v):
        """Parse EXPORT_FORMATS from comma-separated string or list."""
        if isinstance(v, str):
            return [fmt.strip().lower() for fmt in v.split(",")]
        return v
    
    @validator("LOG_LEVEL")
    def validate_log_level(cls, v):
        """Validate log level is one of the allowed values."""
        allowed_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed_levels:
            raise ValueError(f"LOG_LEVEL must be one of {allowed_levels}")
        return v.upper()
    
    @validator("ENVIRONMENT")
    def validate_environment(cls, v):
        """Validate environment is one of the allowed values."""
        allowed_envs = ["development", "staging", "production"]
        if v.lower() not in allowed_envs:
            raise ValueError(f"ENVIRONMENT must be one of {allowed_envs}")
        return v.lower()
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()


# Create settings instance
settings = get_settings()
