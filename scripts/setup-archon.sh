#!/bin/bash

# Archon Setup Script for The Hero Foundry
# Based on official Archon repository recommendations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
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

print_header() {
    echo -e "\n${BLUE}================================${NC}"
    echo -e "${BLUE}  Archon Setup for Hero Foundry${NC}"
    echo -e "${BLUE}================================${NC}\n"
}

# Check if Docker is running
check_docker() {
    print_info "Checking Docker status..."
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Check if Docker Compose is available
check_docker_compose() {
    print_info "Checking Docker Compose..."
    if ! docker-compose --version > /dev/null 2>&1; then
        print_error "Docker Compose is not available. Please install Docker Compose and try again."
        exit 1
    fi
    print_success "Docker Compose is available"
}

# Create necessary directories
create_directories() {
    print_info "Creating necessary directories..."
    
    mkdir -p knowledge-base
    mkdir -p documents
    mkdir -p projects
    mkdir -p uploads
    mkdir -p logs
    
    print_success "Directories created"
}

# Setup environment file
setup_environment() {
    print_info "Setting up environment configuration..."
    
    if [ -f ".env" ]; then
        print_warning ".env file already exists. Backing up to .env.backup"
        cp .env .env.backup
    fi
    
    if [ -f "archon.env.example" ]; then
        cp archon.env.example .env
        print_success "Environment file created from template"
        print_warning "Please edit .env file with your actual API keys and configuration"
    else
        print_error "archon.env.example not found. Please create it first."
        exit 1
    fi
}

# Pull Archon images
pull_images() {
    print_info "Pulling Archon Docker images..."
    
    docker pull ghcr.io/coleam00/archon-ui:latest
    docker pull ghcr.io/coleam00/archon-server:latest
    docker pull ghcr.io/coleam00/archon-mcp:latest
    docker pull ghcr.io/coleam00/archon-agents:latest
    docker pull pgvector/pgvector:pg15
    docker pull redis:7-alpine
    
    print_success "All images pulled successfully"
}

# Start Archon services
start_services() {
    print_info "Starting Archon services..."
    
    docker-compose up -d postgres redis
    
    print_info "Waiting for database to be ready..."
    sleep 10
    
    docker-compose up -d archon-server archon-mcp archon-agents
    
    print_info "Waiting for services to be ready..."
    sleep 15
    
    docker-compose up -d archon-ui
    
    print_success "All services started successfully"
}

# Check service health
check_health() {
    print_info "Checking service health..."
    
    # Check if services are responding
    if curl -f http://localhost:3737 > /dev/null 2>&1; then
        print_success "Archon UI is running on http://localhost:3737"
    else
        print_warning "Archon UI is not responding yet"
    fi
    
    if curl -f http://localhost:8181 > /dev/null 2>&1; then
        print_success "Archon Server is running on http://localhost:8181"
    else
        print_warning "Archon Server is not responding yet"
    fi
    
    if curl -f http://localhost:8051 > /dev/null 2>&1; then
        print_success "Archon MCP Server is running on http://localhost:8051"
    else
        print_warning "Archon MCP Server is not responding yet"
    fi
    
    if curl -f http://localhost:8052 > /dev/null 2>&1; then
        print_success "Archon Agents Service is running on http://localhost:8052"
    else
        print_warning "Archon Agents Service is not responding yet"
    fi
}

# Display connection information
show_connection_info() {
    print_success "\nArchon Setup Complete!"
    echo -e "\n${BLUE}Connection Information:${NC}"
    echo -e "  • Web Interface: ${GREEN}http://localhost:3737${NC}"
    echo -e "  • API Server: ${GREEN}http://localhost:8181${NC}"
    echo -e "  • MCP Server: ${GREEN}http://localhost:8051${NC}"
    echo -e "  • Agents Service: ${GREEN}http://localhost:8052${NC}"
    echo -e "  • Database: ${GREEN}localhost:5432${NC}"
    echo -e "  • Redis: ${GREEN}localhost:6379${NC}"
    
    echo -e "\n${BLUE}For Cursor Integration:${NC}"
    echo -e "  • MCP Server URL: ${GREEN}http://localhost:8051${NC}"
    echo -e "  • Use the MCP Dashboard in Archon UI to get connection details"
    
    echo -e "\n${BLUE}Next Steps:${NC}"
    echo -e "  1. Open http://localhost:3737 in your browser"
    echo -e "  2. Complete the initial setup in the Archon UI"
    echo -e "  3. Add your knowledge base sources"
    echo -e "  4. Configure MCP connection in Cursor"
}

# Main setup function
main() {
    print_header
    
    check_docker
    check_docker_compose
    create_directories
    setup_environment
    pull_images
    start_services
    check_health
    show_connection_info
    
    print_success "\nArchon is now ready for use!"
}

# Run main function
main "$@"
