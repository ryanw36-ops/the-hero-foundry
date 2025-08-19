#!/usr/bin/env python3
"""
Test script to verify Archon connection
Tests all Archon services and MCP connection
"""

import asyncio
import aiohttp
import json
import sys
from typing import Dict, List

# Archon service URLs
ARCHON_SERVICES = {
    "UI": "http://localhost:3737",
    "Server": "http://localhost:8181", 
    "MCP": "http://localhost:8051",
    "Agents": "http://localhost:8052"
}

async def test_service_health(url: str, name: str) -> bool:
    """Test if a service is responding"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                if response.status == 200:
                    print(f"✅ {name}: {url} - Status: {response.status}")
                    return True
                else:
                    print(f"⚠️  {name}: {url} - Status: {response.status}")
                    return False
    except Exception as e:
        print(f"❌ {name}: {url} - Error: {e}")
        return False

async def test_mcp_connection() -> bool:
    """Test MCP server connection"""
    try:
        async with aiohttp.ClientSession() as session:
            # Test MCP server health endpoint
            mcp_url = f"{ARCHON_SERVICES['MCP']}/health"
            async with session.get(mcp_url, timeout=5) as response:
                if response.status == 200:
                    print(f"✅ MCP Server Health Check: {mcp_url}")
                    return True
                else:
                    print(f"⚠️  MCP Server Health Check: Status {response.status}")
                    return False
    except Exception as e:
        print(f"❌ MCP Server Health Check Error: {e}")
        return False

async def test_database_connection() -> bool:
    """Test database connectivity through Archon server"""
    try:
        async with aiohttp.ClientSession() as session:
            # Test database health through Archon server
            db_url = f"{ARCHON_SERVICES['Server']}/health"
            async with session.get(db_url, timeout=5) as response:
                if response.status == 200:
                    print(f"✅ Database Health Check: {db_url}")
                    return True
                else:
                    print(f"⚠️  Database Health Check: Status {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Database Health Check Error: {e}")
        return False

async def test_knowledge_base() -> bool:
    """Test knowledge base functionality"""
    try:
        async with aiohttp.ClientSession() as session:
            # Test knowledge base endpoint
            kb_url = f"{ARCHON_SERVICES['Server']}/api/v1/sources"
            async with session.get(kb_url, timeout=5) as response:
                if response.status == 200:
                    print(f"✅ Knowledge Base: {kb_url}")
                    return True
                else:
                    print(f"⚠️  Knowledge Base: Status {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Knowledge Base Error: {e}")
        return False

async def main():
    """Main test function"""
    print("🚀 Testing Archon Connection for The Hero Foundry")
    print("=" * 60)
    
    # Test all services
    service_results = []
    for name, url in ARCHON_SERVICES.items():
        result = await test_service_health(url, name)
        service_results.append(result)
    
    print("\n" + "=" * 60)
    print("🔍 Testing Specific Functionality")
    print("=" * 60)
    
    # Test specific functionality
    mcp_result = await test_mcp_connection()
    db_result = await test_database_connection()
    kb_result = await test_knowledge_base()
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    # Summary
    all_services = all(service_results)
    all_functionality = all([mcp_result, db_result, kb_result])
    
    if all_services and all_functionality:
        print("🎉 All tests passed! Archon is fully operational.")
        print("\n📋 Next Steps:")
        print("   1. Open Archon UI: http://localhost:3737")
        print("   2. Complete initial setup in the UI")
        print("   3. Configure MCP connection in Cursor")
        print("   4. Start using Archon with your Hero Foundry project!")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        if not all_services:
            print("   - Some Archon services are not responding")
        if not all_functionality:
            print("   - Some functionality tests failed")
        print("\n🔧 Troubleshooting:")
        print("   1. Check if Docker containers are running: docker-compose ps")
        print("   2. Check container logs: docker-compose logs")
        print("   3. Restart services: docker-compose restart")
        print("   4. See ARCHON_SETUP.md for detailed setup instructions")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        sys.exit(1)
