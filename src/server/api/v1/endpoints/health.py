#!/usr/bin/env python3
"""
Health check endpoints for The Hero Foundry backend server.

Provides system health information, database connectivity status, and service monitoring.
"""

import time
from typing import Dict, Any
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db_session_dependency, check_db_health
from ...core.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/")
async def health_check() -> Dict[str, Any]:
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": "The Hero Foundry Backend",
        "version": "2.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": settings.ENVIRONMENT
    }


@router.get("/detailed")
async def detailed_health_check(
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Detailed health check with database connectivity and system status."""
    
    start_time = time.time()
    
    # Check database health
    db_healthy = await check_db_health()
    
    # Calculate response time
    response_time = time.time() - start_time
    
    # Get system information
    import psutil
    import os
    
    system_info = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "process_id": os.getpid(),
        "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}"
    }
    
    # Determine overall health status
    overall_status = "healthy"
    if not db_healthy:
        overall_status = "degraded"
    
    if system_info["memory_percent"] > 90 or system_info["disk_percent"] > 90:
        overall_status = "warning"
    
    return {
        "status": overall_status,
        "service": "The Hero Foundry Backend",
        "version": "2.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": settings.ENVIRONMENT,
        "response_time_ms": round(response_time * 1000, 2),
        "checks": {
            "database": {
                "status": "healthy" if db_healthy else "unhealthy",
                "connected": db_healthy
            },
            "system": {
                "status": "healthy",
                "cpu_usage": f"{system_info['cpu_percent']}%",
                "memory_usage": f"{system_info['memory_percent']}%",
                "disk_usage": f"{system_info['disk_percent']}%"
            }
        },
        "system_info": system_info
    }


@router.get("/ready")
async def readiness_check(
    db: AsyncSession = Depends(get_db_session_dependency)
) -> Dict[str, Any]:
    """Readiness check to determine if the service is ready to handle requests."""
    
    # Check database connectivity
    db_healthy = await check_db_health()
    
    if not db_healthy:
        raise HTTPException(
            status_code=503,
            detail="Service not ready - database connection failed"
        )
    
    return {
        "status": "ready",
        "service": "The Hero Foundry Backend",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": {
            "database": "ready",
            "system": "ready"
        }
    }


@router.get("/live")
async def liveness_check() -> Dict[str, Any]:
    """Liveness check to determine if the service is running."""
    return {
        "status": "alive",
        "service": "The Hero Foundry Backend",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.get("/info")
async def service_info() -> Dict[str, Any]:
    """Get detailed service information and configuration."""
    return {
        "service": {
            "name": "The Hero Foundry Backend",
            "version": "2.0.0",
            "description": "A comprehensive desktop-first D&D character creation application with offline capabilities, AI assistance, and modular ruleset support"
        },
        "configuration": {
            "environment": settings.ENVIRONMENT,
            "debug": settings.DEBUG,
            "log_level": settings.LOG_LEVEL,
            "host": settings.HOST,
            "port": settings.PORT,
            "database_url": settings.DATABASE_URL.replace(settings.DATABASE_URL.split('@')[0].split('://')[1], '***') if '@' in settings.DATABASE_URL else "***",
            "redis_url": settings.REDIS_URL.replace(settings.REDIS_URL.split('@')[0].split('://')[1], '***') if '@' in settings.REDIS_URL else "***"
        },
        "features": {
            "modular_rulesets": True,
            "ai_assistant": bool(settings.OPENAI_API_KEY),
            "offline_support": True,
            "character_creation": True,
            "homebrew_builder": True,
            "export_system": True
        },
        "api_endpoints": {
            "health": "/api/v1/health",
            "characters": "/api/v1/characters",
            "rulesets": "/api/v1/rulesets",
            "homebrew": "/api/v1/homebrew",
            "ai_assistant": "/api/v1/ai"
        },
        "documentation": {
            "swagger_ui": "/docs" if settings.DEBUG else "disabled",
            "redoc": "/redoc" if settings.DEBUG else "disabled",
            "openapi": "/openapi.json" if settings.DEBUG else "disabled"
        }
    }
