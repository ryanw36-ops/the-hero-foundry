#!/usr/bin/env python3
"""
Database connection management for The Hero Foundry backend server.

Handles SQLAlchemy async database connections, connection pooling, and session management.
"""

import asyncio
import logging
from typing import AsyncGenerator, Optional
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session
)
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker

from .config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Global database engine and session factory
_engine: Optional[AsyncEngine] = None
_session_factory: Optional[async_sessionmaker[AsyncSession]] = None


async def init_db() -> None:
    """Initialize database connections and create engine."""
    global _engine, _session_factory
    
    try:
        # Create async engine with connection pooling
        _engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,
            pool_size=settings.DATABASE_POOL_SIZE,
            max_overflow=settings.DATABASE_MAX_OVERFLOW,
            pool_pre_ping=True,
            pool_recycle=3600,  # Recycle connections every hour
        )
        
        # Create session factory
        _session_factory = async_sessionmaker(
            bind=_engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )
        
        # Test database connection
        async with _engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: sync_conn.execute("SELECT 1"))
        
        logger.info("Database connection established successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


async def close_db() -> None:
    """Close database connections and dispose engine."""
    global _engine, _session_factory
    
    try:
        if _engine:
            await _engine.dispose()
            _engine = None
            logger.info("Database engine disposed")
        
        _session_factory = None
        
    except Exception as e:
        logger.error(f"Error closing database connections: {e}")


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Get the database session factory."""
    if not _session_factory:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _session_factory


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session with automatic cleanup."""
    if not _session_factory:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    
    async with _session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_db_session_dependency() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for FastAPI to inject database sessions."""
    async with get_db_session() as session:
        yield session


# Database health check
async def check_db_health() -> bool:
    """Check if database is healthy and responding."""
    try:
        if not _engine:
            return False
        
        async with _engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: sync_conn.execute("SELECT 1"))
        return True
        
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False


# Database initialization for development
async def create_tables() -> None:
    """Create all database tables (development only)."""
    from ..models.base import Base
    
    try:
        if not _engine:
            raise RuntimeError("Database not initialized")
        
        async with _engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Failed to create tables: {e}")
        raise


async def drop_tables() -> None:
    """Drop all database tables (development only)."""
    from ..models.base import Base
    
    try:
        if not _engine:
            raise RuntimeError("Database not initialized")
        
        async with _engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        
        logger.info("Database tables dropped successfully")
        
    except Exception as e:
        logger.error(f"Failed to drop tables: {e}")
        raise
