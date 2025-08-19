#!/usr/bin/env python3
"""
Test all Archon MCP tools
"""

import asyncio
import json
import subprocess
import sys

async def test_tool(tool_name, args=None):
    """Test a single tool"""
    if args is None:
        args = {}
    
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": args
        }
    }
    
    # Start the MCP server
    process = await asyncio.create_subprocess_exec(
        sys.executable, "archon-mcp.py",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    try:
        # Send initialize request first
        init_request = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test", "version": "1.0"}
            }
        }
        
        init_json = json.dumps(init_request) + "\n"
        process.stdin.write(init_json.encode())
        await process.stdin.drain()
        
        # Read initialize response
        init_response = await process.stdout.readline()
        print(f"✅ Initialize response: {init_response.decode().strip()}")
        
        # Send tool call request
        request_json = json.dumps(request) + "\n"
        process.stdin.write(request_json.encode())
        await process.stdin.drain()
        
        # Read response
        response = await process.stdout.readline()
        response_data = json.loads(response.decode().strip())
        
        print(f"✅ Tool {tool_name} response received")
        if "result" in response_data:
            content = response_data["result"]["content"][0]["text"]
            parsed_content = json.loads(content)
            print(f"   Status: {parsed_content.get('status', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing {tool_name}: {e}")
        return False
    finally:
        process.terminate()
        await process.wait()

async def main():
    """Test all tools"""
    print("🧪 Testing Archon MCP Tools...\n")
    
    tests = [
        ("archon_health_check", {"check_type": "basic"}),
        ("archon_session_info", {"include_details": True}),
        ("archon_get_sources", {}),
        ("archon_rag_query", {"query": "How does hero creation work?", "max_results": 3})
    ]
    
    results = []
    for tool_name, args in tests:
        print(f"🔧 Testing {tool_name}...")
        success = await test_tool(tool_name, args)
        results.append(success)
        print()
    
    successful = sum(results)
    total = len(results)
    
    print(f"📊 Test Results: {successful}/{total} tools working correctly")
    
    if successful == total:
        print("🎉 All Archon MCP tools are working perfectly!")
        return True
    else:
        print("⚠️  Some tools need attention")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)


