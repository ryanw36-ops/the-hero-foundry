#!/usr/bin/env python3
"""
Test TCP connection to Archon MCP Server
"""

import socket
import json
import time

def test_tcp_connection():
    """Test connection to TCP MCP server"""
    try:
        # Connect to the server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 8055))
        print("✅ Connected to TCP server on port 8055")
        
        # Test tools/list request
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        
        sock.send((json.dumps(request) + '\n').encode())
        response = sock.recv(1024).decode()
        
        print("✅ Tools list response received:")
        print(f"   {response[:100]}...")
        
        # Test archon_health_check
        health_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "archon_health_check",
                "arguments": {}
            }
        }
        
        sock.send((json.dumps(health_request) + '\n').encode())
        health_response = sock.recv(1024).decode()
        
        print("✅ Health check response received:")
        print(f"   {health_response[:100]}...")
        
        sock.close()
        print("🎉 TCP connection test successful!")
        return True
        
    except Exception as e:
        print(f"❌ TCP connection test failed: {e}")
        return False

if __name__ == "__main__":
    test_tcp_connection()

