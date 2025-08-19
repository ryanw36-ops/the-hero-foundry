# Archon Setup Script for The Hero Foundry (PowerShell)
# Based on official Archon repository recommendations

param(
    [switch]$SkipDockerCheck,
    [switch]$SkipImagePull
)

# Colors for output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Blue"
$White = "White"

# Function to print colored output
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor $Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor $Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor $Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $Red
}

function Write-Header {
    Write-Host "`n================================`n" -ForegroundColor $Blue
    Write-Host "  Archon Setup for Hero Foundry`n" -ForegroundColor $Blue
    Write-Host "================================`n" -ForegroundColor $Blue
}

# Check if Docker is running
function Test-Docker {
    Write-Info "Checking Docker status..."
    try {
        $null = docker info 2>$null
        Write-Success "Docker is running"
        return $true
    }
    catch {
        Write-Error "Docker is not running. Please start Docker Desktop and try again."
        return $false
    }
}

# Check if Docker Compose is available
function Test-DockerCompose {
    Write-Info "Checking Docker Compose..."
    try {
        $version = docker-compose --version 2>$null
        Write-Success "Docker Compose is available: $version"
        return $true
    }
    catch {
        Write-Error "Docker Compose is not available. Please install Docker Compose and try again."
        return $false
    }
}

# Create necessary directories
function New-ArchonDirectories {
    Write-Info "Creating necessary directories..."
    
    $directories = @(
        "knowledge-base",
        "documents", 
        "projects",
        "uploads",
        "logs"
    )
    
    foreach ($dir in $directories) {
        if (!(Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
        }
    }
    
    Write-Success "Directories created"
}

# Setup environment file
function Set-EnvironmentFile {
    Write-Info "Setting up environment configuration..."
    
    if (Test-Path ".env") {
        Write-Warning ".env file already exists. Backing up to .env.backup"
        Copy-Item ".env" ".env.backup" -Force
    }
    
    if (Test-Path "archon.env.example") {
        Copy-Item "archon.env.example" ".env" -Force
        Write-Success "Environment file created from template"
        Write-Warning "Please edit .env file with your actual API keys and configuration"
    }
    else {
        Write-Error "archon.env.example not found. Please create it first."
        exit 1
    }
}

# Pull Archon images
function Pull-ArchonImages {
    if ($SkipImagePull) {
        Write-Warning "Skipping image pull as requested"
        return
    }
    
    Write-Info "Pulling Archon Docker images..."
    
    $images = @(
        "ghcr.io/coleam00/archon-ui:latest",
        "ghcr.io/coleam00/archon-server:latest", 
        "ghcr.io/coleam00/archon-mcp:latest",
        "ghcr.io/coleam00/archon-agents:latest",
        "pgvector/pgvector:pg15",
        "redis:7-alpine"
    )
    
    foreach ($image in $images) {
        Write-Info "Pulling $image..."
        docker pull $image
    }
    
    Write-Success "All images pulled successfully"
}

# Start Archon services
function Start-ArchonServices {
    Write-Info "Starting Archon services..."
    
    # Start database services first
    docker-compose up -d postgres redis
    
    Write-Info "Waiting for database to be ready..."
    Start-Sleep -Seconds 10
    
    # Start core services
    docker-compose up -d archon-server archon-mcp archon-agents
    
    Write-Info "Waiting for services to be ready..."
    Start-Sleep -Seconds 15
    
    # Start UI last
    docker-compose up -d archon-ui
    
    Write-Success "All services started successfully"
}

# Check service health
function Test-ServiceHealth {
    Write-Info "Checking service health..."
    
    $services = @{
        "Archon UI" = "http://localhost:3737"
        "Archon Server" = "http://localhost:8181"
        "Archon MCP Server" = "http://localhost:8051"
        "Archon Agents Service" = "http://localhost:8052"
    }
    
    foreach ($service in $services.GetEnumerator()) {
        try {
            $response = Invoke-WebRequest -Uri $service.Value -UseBasicParsing -TimeoutSec 5
            if ($response.StatusCode -eq 200) {
                Write-Success "$($service.Key) is running on $($service.Value)"
            }
        }
        catch {
            Write-Warning "$($service.Key) is not responding yet"
        }
    }
}

# Display connection information
function Show-ConnectionInfo {
    Write-Success "`nArchon Setup Complete!"
    Write-Host "`nConnection Information:" -ForegroundColor $Blue
    Write-Host "  • Web Interface: http://localhost:3737" -ForegroundColor $Green
    Write-Host "  • API Server: http://localhost:8181" -ForegroundColor $Green
    Write-Host "  • MCP Server: http://localhost:8051" -ForegroundColor $Green
    Write-Host "  • Agents Service: http://localhost:8052" -ForegroundColor $Green
    Write-Host "  • Database: localhost:5432" -ForegroundColor $Green
    Write-Host "  • Redis: localhost:6379" -ForegroundColor $Green
    
    Write-Host "`nFor Cursor Integration:" -ForegroundColor $Blue
    Write-Host "  • MCP Server URL: http://localhost:8051" -ForegroundColor $Green
    Write-Host "  • Use the MCP Dashboard in Archon UI to get connection details"
    
    Write-Host "`nNext Steps:" -ForegroundColor $Blue
    Write-Host "  1. Open http://localhost:3737 in your browser" -ForegroundColor $White
    Write-Host "  2. Complete the initial setup in the Archon UI" -ForegroundColor $White
    Write-Host "  3. Add your knowledge base sources" -ForegroundColor $White
    Write-Host "  4. Configure MCP connection in Cursor" -ForegroundColor $White
}

# Main setup function
function Start-ArchonSetup {
    Write-Header
    
    if (!$SkipDockerCheck) {
        if (!(Test-Docker)) { exit 1 }
        if (!(Test-DockerCompose)) { exit 1 }
    }
    
    New-ArchonDirectories
    Set-EnvironmentFile
    Pull-ArchonImages
    Start-ArchonServices
    Test-ServiceHealth
    Show-ConnectionInfo
    
    Write-Success "`nArchon is now ready for use!"
}

# Run main setup
Start-ArchonSetup
