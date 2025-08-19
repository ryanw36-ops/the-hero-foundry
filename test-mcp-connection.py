#!/usr/bin/env python3
"""
Test script to verify MCP server connection
"""

import requests
import json

def test_mcp_server():
    """Test the MCP server endpoints"""
    base_url = "http://localhost:8053"
    
    print("Testing MCP Server Connection...")
    print(f"Base URL: {base_url}")
    print("-" * 50)
    
    # Test health endpoint
    try:
        print("1. Testing health endpoint...")
        response = requests.get(f"{base_url}/mcp/health", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test tools endpoint
    try:
        print("2. Testing tools endpoint...")
        response = requests.get(f"{base_url}/mcp/tools", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test tool call endpoint
    try:
        print("3. Testing tool call endpoint...")
        test_data = {
            "name": "archon_health_check",
            "arguments": {
                "random_string": "test"
            }
        }
        response = requests.post(f"{base_url}/mcp/call", 
                               json=test_data, 
                               timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_mcp_server()

