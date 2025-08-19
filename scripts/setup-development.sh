#!/bin/bash

# =============================================================================
# The Hero Foundry - Development Environment Setup Script
# =============================================================================
# This script automates the setup of the development environment
# Run this script from the project root directory

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python_version() {
    if command_exists python3; then
        python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
        if [[ "$python_version" == "3.11" ]]; then
            print_success "Python 3.11 found: $(python3 --version)"
            return 0
        else
            print_warning "Python $python_version found, but Python 3.11 is recommended"
            return 1
        fi
    else
        print_error "Python 3 not found. Please install Python 3.11+"
        return 1
    fi
}

# Function to check Node.js version
check_node_version() {
    if command_exists node; then
        node_version=$(node --version | cut -d'v' -f2 | cut -d. -f1)
        if [[ "$node_version" -ge 18 ]]; then
            print_success "Node.js $(node --version) found"
            return 0
        else
            print_error "Node.js $(node --version) found, but Node.js 18+ is required"
            return 1
        fi
    else
        print_error "Node.js not found. Please install Node.js 18+"
        return 1
    fi
}

# Function to check Docker
check_docker() {
    if command_exists docker; then
        if docker info >/dev/null 2>&1; then
            print_success "Docker is running"
            return 0
        else
            print_error "Docker is installed but not running. Please start Docker Desktop"
            return 1
        fi
    else
        print_error "Docker not found. Please install Docker Desktop"
        return 1
    fi
}

# Function to create virtual environment
setup_python_env() {
    print_status "Setting up Python virtual environment..."
    
    if [[ ! -d ".venv" ]]; then
        python3 -m venv .venv
        print_success "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source .venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install requirements
    if [[ -f "requirements.txt" ]]; then
        print_status "Installing Python dependencies..."
        pip install -r requirements.txt
        print_success "Python dependencies installed"
    else
        print_warning "requirements.txt not found, skipping Python dependency installation"
    fi
}

# Function to setup Node.js dependencies
setup_node_env() {
    print_status "Setting up Node.js environment..."
    
    if [[ -f "package.json" ]]; then
        print_status "Installing Node.js dependencies..."
        npm install
        print_success "Node.js dependencies installed"
    else
        print_warning "package.json not found, skipping Node.js dependency installation"
    fi
}

# Function to setup environment file
setup_env_file() {
    print_status "Setting up environment configuration..."
    
    if [[ ! -f ".env" ]]; then
        if [[ -f "docs/setup/env-template.txt" ]]; then
            cp docs/setup/env-template.txt .env
            print_success "Environment file created from template"
            print_warning "Please edit .env file with your configuration values"
        else
            print_warning "Environment template not found, creating basic .env file"
            cat > .env << EOF
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
EOF
            print_success "Basic environment file created"
        fi
    else
        print_status "Environment file already exists"
    fi
}

# Function to start database services
start_database_services() {
    print_status "Starting database services with Docker..."
    
    if [[ -f "docker-compose.dev.yml" ]]; then
        # Start only the database services
        docker-compose -f docker-compose.dev.yml up -d postgres redis
        
        # Wait for services to be ready
        print_status "Waiting for database services to be ready..."
        sleep 10
        
        # Check service status
        if docker-compose -f docker-compose.dev.yml ps | grep -q "Up"; then
            print_success "Database services started successfully"
        else
            print_error "Failed to start database services"
            return 1
        fi
    else
        print_error "docker-compose.dev.yml not found"
        return 1
    fi
}

# Function to initialize database
initialize_database() {
    print_status "Initializing database..."
    
    # Activate virtual environment if not already activated
    if [[ -z "$VIRTUAL_ENV" ]]; then
        source .venv/bin/activate
    fi
    
    # Check if database initialization script exists
    if [[ -f "database/init/01-init-database.sql" ]]; then
        print_status "Database initialization script found"
        print_warning "Database initialization requires manual execution"
        print_status "Please run: docker-compose -f docker-compose.dev.yml exec postgres psql -U hero_foundry -d hero_foundry -f /docker-entrypoint-initdb.d/01-init-database.sql"
    else
        print_warning "Database initialization script not found"
    fi
}

# Function to run tests
run_tests() {
    print_status "Running environment tests..."
    
    # Activate virtual environment if not already activated
    if [[ -z "$VIRTUAL_ENV" ]]; then
        source .venv/bin/activate
    fi
    
    if [[ -f "scripts/test-database-connection.py" ]]; then
        print_status "Running database connection tests..."
        python scripts/test-database-connection.py
    else
        print_warning "Database test script not found"
    fi
}

# Function to print next steps
print_next_steps() {
    echo
    echo "=============================================================================="
    echo "🎉 Development Environment Setup Complete!"
    echo "=============================================================================="
    echo
    echo "🚀 Next steps:"
    echo "   1. Edit your .env file with your configuration values"
    echo "   2. Start your development servers:"
    echo "      - Backend: npm run dev:backend"
    echo "      - Frontend: npm run dev:frontend"
    echo "      - Desktop: npm run dev:desktop"
    echo "   3. Open the application:"
    echo "      - API Docs: http://localhost:8000/docs"
    echo "      - Frontend: http://localhost:3000"
    echo "      - pgAdmin: http://localhost:5050 (admin@herofoundry.local / admin)"
    echo "      - Redis Commander: http://localhost:8081 (admin / admin)"
    echo
    echo "📚 Documentation:"
    echo "   - Development Guide: docs/setup/development-environment.md"
    echo "   - Architecture: docs/fullstack-architecture.md"
    echo
    echo "🔧 Troubleshooting:"
    echo "   - Check container logs: docker-compose -f docker-compose.dev.yml logs"
    echo "   - Run tests: python scripts/test-database-connection.py"
    echo "   - Restart services: docker-compose -f docker-compose.dev.yml restart"
    echo
    echo "Happy coding! 🎲⚔️✨"
    echo
}

# Main setup function
main() {
    echo "=============================================================================="
    echo "🚀 The Hero Foundry - Development Environment Setup"
    echo "=============================================================================="
    echo
    
    # Check prerequisites
    print_status "Checking prerequisites..."
    
    check_python_version
    check_node_version
    check_docker
    
    # Setup environment
    print_status "Setting up development environment..."
    
    setup_python_env
    setup_node_env
    setup_env_file
    
    # Start services
    print_status "Starting development services..."
    
    start_database_services
    initialize_database
    
    # Run tests
    run_tests
    
    # Print next steps
    print_next_steps
}

# Check if script is run from project root
if [[ ! -f "docs/setup/development-environment.md" ]]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Run main setup
main "$@"
