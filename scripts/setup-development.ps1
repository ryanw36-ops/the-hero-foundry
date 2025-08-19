# =============================================================================
# The Hero Foundry - Development Environment Setup Script (PowerShell)
# =============================================================================
# This script automates the setup of the development environment on Windows
# Run this script from the project root directory

param(
    [switch]$SkipChecks,
    [switch]$SkipDocker,
    [switch]$Help
)

if ($Help) {
    Write-Host @"
The Hero Foundry - Development Environment Setup Script

Usage: .\scripts\setup-development.ps1 [options]

Options:
    -SkipChecks    Skip prerequisite checks
    -SkipDocker   Skip Docker service startup
    -Help         Show this help message

Examples:
    .\scripts\setup-development.ps1
    .\scripts\setup-development.ps1 -SkipChecks
    .\scripts\setup-development.ps1 -SkipDocker
"@
    exit 0
}

# Set error action preference
$ErrorActionPreference = "Stop"

# Function to print colored output
function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Function to check if command exists
function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Function to check Python version
function Test-PythonVersion {
    if (Test-Command "python") {
        try {
            $pythonVersion = python --version 2>&1
            if ($pythonVersion -match "Python 3\.11") {
                Write-Success "Python 3.11 found: $pythonVersion"
                return $true
            }
            else {
                Write-Warning "Python found: $pythonVersion, but Python 3.11 is recommended"
                return $false
            }
        }
        catch {
            Write-Error "Failed to get Python version"
            return $false
        }
    }
    else {
        Write-Error "Python not found. Please install Python 3.11+"
        return $false
    }
}

# Function to check Node.js version
function Test-NodeVersion {
    if (Test-Command "node") {
        try {
            $nodeVersion = node --version
            $majorVersion = [int]($nodeVersion -replace 'v', '' -split '\.')[0]
            if ($majorVersion -ge 18) {
                Write-Success "Node.js $nodeVersion found"
                return $true
            }
            else {
                Write-Error "Node.js $nodeVersion found, but Node.js 18+ is required"
                return $false
            }
        }
        catch {
            Write-Error "Failed to get Node.js version"
            return $false
        }
    }
    else {
        Write-Error "Node.js not found. Please install Node.js 18+"
        return $false
    }
}

# Function to check Docker
function Test-Docker {
    if (Test-Command "docker") {
        try {
            docker info | Out-Null
            Write-Success "Docker is running"
            return $true
        }
        catch {
            Write-Error "Docker is installed but not running. Please start Docker Desktop"
            return $false
        }
    }
    else {
        Write-Error "Docker not found. Please install Docker Desktop"
        return $false
    }
}

# Function to create virtual environment
function Initialize-PythonEnv {
    Write-Status "Setting up Python virtual environment..."
    
    if (-not (Test-Path ".venv")) {
        python -m venv .venv
        Write-Success "Virtual environment created"
    }
    else {
        Write-Status "Virtual environment already exists"
    }
    
    # Activate virtual environment
    & ".venv\Scripts\Activate.ps1"
    
    # Upgrade pip
    python -m pip install --upgrade pip
    
    # Install requirements
    if (Test-Path "requirements.txt") {
        Write-Status "Installing Python dependencies..."
        pip install -r requirements.txt
        Write-Success "Python dependencies installed"
    }
    else {
        Write-Warning "requirements.txt not found, skipping Python dependency installation"
    }
}

# Function to setup Node.js dependencies
function Initialize-NodeEnv {
    Write-Status "Setting up Node.js environment..."
    
    if (Test-Path "package.json") {
        Write-Status "Installing Node.js dependencies..."
        npm install
        Write-Success "Node.js dependencies installed"
    }
    else {
        Write-Warning "package.json not found, skipping Node.js dependency installation"
    }
}

# Function to setup environment file
function Initialize-EnvFile {
    Write-Status "Setting up environment configuration..."
    
    if (-not (Test-Path ".env")) {
        if (Test-Path "docs\setup\env-template.txt") {
            Copy-Item "docs\setup\env-template.txt" ".env"
            Write-Success "Environment file created from template"
            Write-Warning "Please edit .env file with your configuration values"
        }
        else {
            Write-Warning "Environment template not found, creating basic .env file"
            @"
# The Hero Foundry Development Environment
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# Database Configuration
DATABASE_URL=postgresql://hero_foundry:password@localhost:5432/hero_foundry
REDIS_URL=redis://localhost:6379

# Server Configuration
BACKEND_PORT=8000
FRONTEND_PORT=3000

# AI Provider (Optional)
AI_PROVIDER_API_KEY=your_api_key_here

# Security
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
"@ | Out-File -FilePath ".env" -Encoding UTF8
            Write-Success "Basic environment file created"
        }
    }
    else {
        Write-Status "Environment file already exists"
    }
}

# Function to start database services
function Start-DatabaseServices {
    if ($SkipDocker) {
        Write-Warning "Skipping Docker service startup"
        return
    }
    
    Write-Status "Starting database services with Docker..."
    
    if (Test-Path "docker-compose.dev.yml") {
        # Start only the database services
        docker-compose -f docker-compose.dev.yml up -d postgres redis
        
        # Wait for services to be ready
        Write-Status "Waiting for database services to be ready..."
        Start-Sleep -Seconds 10
        
        # Check service status
        $services = docker-compose -f docker-compose.dev.yml ps
        if ($services -match "Up") {
            Write-Success "Database services started successfully"
        }
        else {
            Write-Error "Failed to start database services"
            throw "Database services failed to start"
        }
    }
    else {
        Write-Error "docker-compose.dev.yml not found"
        throw "Docker compose file not found"
    }
}

# Function to initialize database
function Initialize-Database {
    Write-Status "Initializing database..."
    
    # Check if database initialization script exists
    if (Test-Path "database\init\01-init-database.sql") {
        Write-Status "Database initialization script found"
        Write-Warning "Database initialization requires manual execution"
        Write-Status "Please run: docker-compose -f docker-compose.dev.yml exec postgres psql -U hero_foundry -d hero_foundry -f /docker-entrypoint-initdb.d/01-init-database.sql"
    }
    else {
        Write-Warning "Database initialization script not found"
    }
}

# Function to run tests
function Invoke-Tests {
    Write-Status "Running environment tests..."
    
    if (Test-Path "scripts\test-database-connection.py") {
        Write-Status "Running database connection tests..."
        python scripts\test-database-connection.py
    }
    else {
        Write-Warning "Database test script not found"
    }
}

# Function to print next steps
function Write-NextSteps {
    Write-Host ""
    Write-Host "==============================================================================" -ForegroundColor Cyan
    Write-Host "🎉 Development Environment Setup Complete!" -ForegroundColor Green
    Write-Host "==============================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🚀 Next steps:" -ForegroundColor Yellow
    Write-Host "   1. Edit your .env file with your configuration values"
    Write-Host "   2. Start your development servers:"
    Write-Host "      - Backend: npm run dev:backend"
    Write-Host "      - Frontend: npm run dev:frontend"
    Write-Host "      - Desktop: npm run dev:desktop"
    Write-Host "   3. Open the application:"
    Write-Host "      - API Docs: http://localhost:8000/docs"
    Write-Host "      - Frontend: http://localhost:3000"
    Write-Host "      - pgAdmin: http://localhost:5050 (admin@herofoundry.local / admin)"
    Write-Host "      - Redis Commander: http://localhost:8081 (admin / admin)"
    Write-Host ""
    Write-Host "📚 Documentation:" -ForegroundColor Yellow
    Write-Host "   - Development Guide: docs\setup\development-environment.md"
    Write-Host "   - Architecture: docs\fullstack-architecture.md"
    Write-Host ""
    Write-Host "🔧 Troubleshooting:" -ForegroundColor Yellow
    Write-Host "   - Check container logs: docker-compose -f docker-compose.dev.yml logs"
    Write-Host "   - Run tests: python scripts\test-database-connection.py"
    Write-Host "   - Restart services: docker-compose -f docker-compose.dev.yml restart"
    Write-Host ""
    Write-Host "Happy coding! 🎲⚔️✨" -ForegroundColor Green
    Write-Host ""
}

# Main setup function
function Main {
    Write-Host "==============================================================================" -ForegroundColor Cyan
    Write-Host "🚀 The Hero Foundry - Development Environment Setup" -ForegroundColor Cyan
    Write-Host "==============================================================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Check prerequisites
    if (-not $SkipChecks) {
        Write-Status "Checking prerequisites..."
        
        Test-PythonVersion
        Test-NodeVersion
        Test-Docker
    }
    
    # Setup environment
    Write-Status "Setting up development environment..."
    
    Initialize-PythonEnv
    Initialize-NodeEnv
    Initialize-EnvFile
    
    # Start services
    Write-Status "Starting development services..."
    
    Start-DatabaseServices
    Initialize-Database
    
    # Run tests
    Invoke-Tests
    
    # Print next steps
    Write-NextSteps
}

# Check if script is run from project root
if (-not (Test-Path "docs\setup\development-environment.md")) {
    Write-Error "Please run this script from the project root directory"
    exit 1
}

# Run main setup
try {
    Main
}
catch {
    Write-Error "Setup failed: $($_.Exception.Message)"
    Write-Host ""
    Write-Host "🔧 Troubleshooting tips:" -ForegroundColor Yellow
    Write-Host "   - Ensure Docker Desktop is running"
    Write-Host "   - Check that all prerequisites are installed"
    Write-Host "   - Verify you're running from the project root directory"
    Write-Host "   - Check the error message above for specific issues"
    exit 1
}
