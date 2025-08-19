#!/usr/bin/env python3
"""
Main API router for The Hero Foundry backend server.

Includes all endpoint routers and defines the overall API structure.
"""

from fastapi import APIRouter

from .endpoints import characters, rulesets, homebrew, ai_assistant, health

# Create the main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    health.router,
    prefix="/health",
    tags=["health"]
)

api_router.include_router(
    characters.router,
    prefix="/characters",
    tags=["characters"]
)

api_router.include_router(
    rulesets.router,
    prefix="/rulesets",
    tags=["rulesets"]
)

api_router.include_router(
    homebrew.router,
    prefix="/homebrew",
    tags=["homebrew"]
)

api_router.include_router(
    ai_assistant.router,
    prefix="/ai",
    tags=["ai_assistant"]
)

# Root API endpoint
@api_router.get("/")
async def api_root():
    """Root endpoint for the API."""
    return {
        "message": "The Hero Foundry API v1",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "characters": "/characters",
            "rulesets": "/rulesets",
            "homebrew": "/homebrew",
            "ai_assistant": "/ai"
        }
    }
