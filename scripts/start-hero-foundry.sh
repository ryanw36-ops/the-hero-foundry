#!/bin/bash

# The Hero Foundry - Docker Startup Script
echo "🚀 Starting The Hero Foundry with Archon Integration..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build and start the containers
echo "🔨 Building and starting containers..."
docker-compose -f docker-compose.hero-foundry.yml up --build -d

# Wait for containers to be ready
echo "⏳ Waiting for containers to be ready..."
sleep 10

# Check container status
echo "📊 Container Status:"
docker-compose -f docker-compose.hero-foundry.yml ps

# Test MCP connection
echo "🔌 Testing MCP connection..."
sleep 5

# Show logs
echo "📋 Recent logs:"
docker-compose -f docker-compose.hero-foundry.yml logs --tail=20

echo "✅ The Hero Foundry is now running!"
echo "🌐 MCP Server: http://localhost:8054/mcp"
echo "🏗️  Main App: http://localhost:8001"
echo "🗄️  Database: localhost:5433"
echo "🔴 Redis: localhost:6380"
echo ""
echo "📖 To view logs: docker-compose -f docker-compose.hero-foundry.yml logs -f"
echo "🛑 To stop: docker-compose -f docker-compose.hero-foundry.yml down"


