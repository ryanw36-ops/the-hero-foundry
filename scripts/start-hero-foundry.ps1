# The Hero Foundry - Docker Startup Script (PowerShell)
Write-Host "🚀 Starting The Hero Foundry with Archon Integration..." -ForegroundColor Green

# Check if Docker is running
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Docker is not running. Please start Docker first." -ForegroundColor Red
    exit 1
}

# Build and start the containers
Write-Host "🔨 Building and starting containers..." -ForegroundColor Yellow
docker-compose -f docker-compose.hero-foundry.yml up --build -d

# Wait for containers to be ready
Write-Host "⏳ Waiting for containers to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check container status
Write-Host "📊 Container Status:" -ForegroundColor Cyan
docker-compose -f docker-compose.hero-foundry.yml ps

# Test MCP connection
Write-Host "🔌 Testing MCP connection..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Show logs
Write-Host "📋 Recent logs:" -ForegroundColor Cyan
docker-compose -f docker-compose.hero-foundry.yml logs --tail=20

Write-Host "✅ The Hero Foundry is now running!" -ForegroundColor Green
Write-Host "🌐 MCP Server: http://localhost:8054/mcp" -ForegroundColor White
Write-Host "🏗️  Main App: http://localhost:8001" -ForegroundColor White
Write-Host "🗄️  Database: localhost:5433" -ForegroundColor White
Write-Host "🔴 Redis: localhost:6380" -ForegroundColor White
Write-Host ""
Write-Host "📖 To view logs: docker-compose -f docker-compose.hero-foundry.yml logs -f" -ForegroundColor Gray
Write-Host "🛑 To stop: docker-compose -f docker-compose.hero-foundry.yml down" -ForegroundColor Gray


