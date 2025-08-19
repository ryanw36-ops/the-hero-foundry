#!/usr/bin/env python3
"""
Startup script for The Hero Foundry backend server.

This script initializes and starts the FastAPI server for development.
"""

import uvicorn
import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from server.main import app

if __name__ == "__main__":
    print("🚀 Starting The Hero Foundry Backend Server...")
    print("📖 API Documentation will be available at: http://localhost:8000/docs")
    print("🔍 Health check available at: http://localhost:8000/health")
    
    uvicorn.run(
        "server.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
