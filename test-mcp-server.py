#!/usr/bin/env python3
"""
Test script to verify the MCP server works
"""

import asyncio
import json
import subprocess
import sys
from mcp.client.stdio import stdio_client

async def test_mcp_server():
    """Test the MCP server by connecting to it"""
    print("Testing MCP Server...")
    
    try:
        # Start the MCP server process
        server_process = await asyncio.create_subprocess_exec(
            sys.executable, "proper-mcp-server.py",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Connect to the server
        async with stdio_client(server_process.stdin, server_process.stdout) as (read, write):
            print("✅ Connected to MCP server successfully!")
            
            # Test listing tools
            from mcp.client.session import ClientSession
            session = ClientSession(read, write)
            
            await session.initialize()
            print("✅ Session initialized successfully!")
            
            # List available tools
            tools = await session.list_tools()
            print(f"✅ Found {len(tools.tools)} tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # Test a tool call
            if tools.tools:
                tool = tools.tools[0]  # Test the first tool
                print(f"\n🔧 Testing tool: {tool.name}")
                
                # Call the health check tool
                result = await session.call_tool(
                    tool.name,
                    {"check_type": "basic"} if tool.name == "archon_health_check" else {}
                )
                
                print(f"✅ Tool call successful!")
                for content in result.content:
                    if hasattr(content, 'text'):
                        print(f"Response: {content.text[:200]}...")
            
        # Terminate the server process
        server_process.terminate()
        await server_process.wait()
        
        print("\n🎉 MCP Server test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_mcp_server())
    sys.exit(0 if success else 1)


