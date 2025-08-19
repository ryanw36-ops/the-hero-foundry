# Quick Start Script for Archon
# Run this to start Archon services

Write-Host "🚀 Starting Archon for The Hero Foundry..." -ForegroundColor Green

# Check if Docker is running
try {
    $null = docker info 2>$null
    Write-Host "✅ Docker is running" -ForegroundColor Green
}
catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if .env file exists
if (!(Test-Path ".env")) {
    Write-Host "⚠️  .env file not found. Creating from template..." -ForegroundColor Yellow
    if (Test-Path "archon.env.example") {
        Copy-Item "archon.env.example" ".env"
        Write-Host "✅ Environment file created. Please edit .env with your API keys." -ForegroundColor Yellow
    }
    else {
        Write-Host "❌ archon.env.example not found. Please run setup-archon.ps1 first." -ForegroundColor Red
        exit 1
    }
}

# Start Archon services
Write-Host "🔧 Starting Archon services..." -ForegroundColor Blue
docker-compose up -d

Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 20

# Check service status
Write-Host "🔍 Checking service status..." -ForegroundColor Blue
docker-compose ps

Write-Host "`n🎉 Archon is starting up!" -ForegroundColor Green
Write-Host "`n📋 Access your services:" -ForegroundColor White
Write-Host "   • Web Interface: http://localhost:3737" -ForegroundColor Cyan
Write-Host "   • API Server: http://localhost:8181" -ForegroundColor Cyan
Write-Host "   • MCP Server: http://localhost:8051" -ForegroundColor Cyan
Write-Host "   • Agents Service: http://localhost:8052" -ForegroundColor Cyan

Write-Host "`n🔗 For Cursor integration:" -ForegroundColor White
Write-Host "   1. Open http://localhost:3737" -ForegroundColor Cyan
Write-Host "   2. Go to MCP Dashboard" -ForegroundColor Cyan
Write-Host "   3. Copy connection details for Cursor" -ForegroundColor Cyan

Write-Host "`n💡 Run 'python test-archon-connection.py' to test the connection" -ForegroundColor Yellow
