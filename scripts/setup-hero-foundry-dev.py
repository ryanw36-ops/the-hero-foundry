#!/usr/bin/env python3
"""
The Hero Foundry - Development Environment Setup Script
======================================================

This script automates the setup of the development environment for The Hero Foundry.
It sets up Docker services, database initialization, and validates the environment.

Requirements:
- Python 3.11+
- Docker Desktop running
- Node.js 18+
"""

import os
import sys
import subprocess
import time
import json
import platform
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_status(message: str, color: str = Colors.OKBLUE):
    """Print a status message with color."""
    print(f"{color}[INFO]{Colors.ENDC} {message}")

def print_success(message: str):
    """Print a success message."""
    print(f"{Colors.OKGREEN}[SUCCESS]{Colors.ENDC} {message}")

def print_warning(message: str):
    """Print a warning message."""
    print(f"{Colors.WARNING}[WARNING]{Colors.ENDC} {message}")

def print_error(message: str):
    """Print an error message."""
    print(f"{Colors.FAIL}[ERROR]{Colors.ENDC} {message}")

def print_header(message: str):
    """Print a header message."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{message}{Colors.ENDC}")
    print("=" * len(message))

def check_python_version() -> bool:
    """Check if Python version meets requirements."""
    print_status("Checking Python version...")
    
    if sys.version_info < (3, 11):
        print_error(f"Python 3.11+ required, found {sys.version}")
        return False
    
    print_success(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} found")
    return True

def check_docker() -> bool:
    """Check if Docker is available and running."""
    print_status("Checking Docker...")
    
    try:
        result = subprocess.run(['docker', 'info'], capture_output=True, text=True, check=True)
        if 'Server Version' in result.stdout:
            print_success("Docker is running")
            return True
        else:
            print_error("Docker is not running properly")
            return False
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("Docker not found or not running. Please start Docker Desktop")
        return False

def check_docker_compose() -> bool:
    """Check if Docker Compose is available."""
    print_status("Checking Docker Compose...")
    
    try:
        result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True, check=True)
        print_success(f"Docker Compose: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("Docker Compose not found")
        return False

def check_node_version() -> bool:
    """Check if Node.js version meets requirements."""
    print_status("Checking Node.js version...")
    
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, check=True)
        version = result.stdout.strip()
        major_version = int(version.split('.')[0].replace('v', ''))
        
        if major_version >= 18:
            print_success(f"Node.js {version} found")
            return True
        else:
            print_error(f"Node.js 18+ required, found {version}")
            return False
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("Node.js not found. Please install Node.js 18+")
        return False

def create_directories() -> None:
    """Create necessary directories for the project."""
    print_status("Creating project directories...")
    
    directories = [
        'storage',
        'content/rulesets',
        'content/homebrew',
        'exports',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print_status(f"Created directory: {directory}")
    
    print_success("Project directories created")

def start_database_services() -> bool:
    """Start the database services using Docker Compose."""
    print_status("Starting database services...")
    
    try:
        # Start only the core services (postgres, redis)
        result = subprocess.run([
            'docker-compose', '-f', 'docker-compose.dev.yml', 'up', '-d', 'postgres', 'redis'
        ], capture_output=True, text=True, check=True)
        
        print_success("Database services started")
        
        # Wait for services to be ready
        print_status("Waiting for services to be ready...")
        time.sleep(15)
        
        # Check service status
        result = subprocess.run([
            'docker-compose', '-f', 'docker-compose.dev.yml', 'ps'
        ], capture_output=True, text=True, check=True)
        
        if 'Up' in result.stdout:
            print_success("All services are running")
            return True
        else:
            print_error("Some services failed to start")
            return False
            
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to start services: {e}")
        return False

def start_optional_services() -> bool:
    """Start optional development tools."""
    print_status("Starting optional development tools...")
    
    try:
        # Start tools profile (pgAdmin, Redis Commander, MailHog)
        result = subprocess.run([
            'docker-compose', '-f', 'docker-compose.dev.yml', '--profile', 'tools', 'up', '-d'
        ], capture_output=True, text=True, check=True)
        
        print_success("Optional services started")
        return True
        
    except subprocess.CalledProcessError as e:
        print_warning(f"Failed to start optional services: {e}")
        return False

def test_database_connection() -> bool:
    """Test the database connection."""
    print_status("Testing database connection...")
    
    try:
        # Test PostgreSQL connection
        result = subprocess.run([
            'docker-compose', '-f', 'docker-compose.dev.yml', 'exec', '-T', 'postgres',
            'pg_isready', '-U', 'hero_foundry', '-d', 'hero_foundry'
        ], capture_output=True, text=True, check=True)
        
        if 'accepting connections' in result.stdout:
            print_success("PostgreSQL connection successful")
        else:
            print_error("PostgreSQL connection failed")
            return False
        
        # Test Redis connection
        result = subprocess.run([
            'docker-compose', '-f', 'docker-compose.dev.yml', 'exec', '-T', 'redis',
            'redis-cli', 'ping'
        ], capture_output=True, text=True, check=True)
        
        if 'PONG' in result.stdout:
            print_success("Redis connection successful")
        else:
            print_error("Redis connection failed")
            return False
        
        return True
        
    except subprocess.CalledProcessError as e:
        print_error(f"Database connection test failed: {e}")
        return False

def initialize_database() -> bool:
    """Initialize the database with schema and sample data."""
    print_status("Initializing database...")
    
    try:
        # Run the database initialization script
        result = subprocess.run([
            'docker-compose', '-f', 'docker-compose.dev.yml', 'exec', '-T', 'postgres',
            'psql', '-U', 'hero_foundry', '-d', 'hero_foundry', '-f', '/docker-entrypoint-initdb.d/01-init-database.sql'
        ], capture_output=True, text=True, check=True)
        
        if 'Database initialization completed successfully' in result.stdout:
            print_success("Database initialized successfully")
            return True
        else:
            print_warning("Database initialization may have had issues")
            return False
            
    except subprocess.CalledProcessError as e:
        print_error(f"Database initialization failed: {e}")
        return False

def setup_python_environment() -> bool:
    """Set up the Python virtual environment and dependencies."""
    print_status("Setting up Python environment...")
    
    try:
        # Create virtual environment if it doesn't exist
        if not Path('.venv').exists():
            subprocess.run([sys.executable, '-m', 'venv', '.venv'], check=True)
            print_success("Virtual environment created")
        else:
            print_status("Virtual environment already exists")
        
        # Determine the correct activation script
        if platform.system() == "Windows":
            activate_script = Path('.venv/Scripts/activate')
            pip_path = Path('.venv/Scripts/pip')
        else:
            activate_script = Path('.venv/bin/activate')
            pip_path = Path('.venv/bin/pip')
        
        # Install requirements
        if Path('requirements.txt').exists():
            subprocess.run([str(pip_path), 'install', '-r', 'requirements.txt'], check=True)
            print_success("Python dependencies installed")
        else:
            print_warning("requirements.txt not found")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print_error(f"Python environment setup failed: {e}")
        return False

def setup_node_environment() -> bool:
    """Set up the Node.js environment and dependencies."""
    print_status("Setting up Node.js environment...")
    
    try:
        # Check if we're in the hero-foundry directory
        if Path('hero-foundry/package.json').exists():
            os.chdir('hero-foundry')
            subprocess.run(['npm', 'install'], check=True)
            print_success("Node.js dependencies installed")
            os.chdir('..')
            return True
        else:
            print_warning("hero-foundry/package.json not found")
            return False
            
    except subprocess.CalledProcessError as e:
        print_error(f"Node.js environment setup failed: {e}")
        return False

def print_service_urls() -> None:
    """Print the URLs for accessing various services."""
    print_header("Development Environment Services")
    
    services = {
        "PostgreSQL Database": "localhost:5432",
        "Redis Cache": "localhost:6379",
        "pgAdmin (Database UI)": "http://localhost:5050",
        "Redis Commander": "http://localhost:8081",
        "MailHog (Email Testing)": "http://localhost:8025",
        "Frontend (React)": "http://localhost:3000",
        "Backend API": "http://localhost:8000"
    }
    
    for service, url in services.items():
        print(f"  {service}: {Colors.OKCYAN}{url}{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}Database Credentials:{Colors.ENDC}")
    print(f"  Username: {Colors.OKCYAN}hero_foundry{Colors.ENDC}")
    print(f"  Password: {Colors.OKCYAN}password{Colors.ENDC}")
    print(f"  Database: {Colors.OKCYAN}hero_foundry{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}pgAdmin Credentials:{Colors.ENDC}")
    print(f"  Email: {Colors.OKCYAN}admin@herofoundry.local{Colors.ENDC}")
    print(f"  Password: {Colors.OKCYAN}admin{Colors.ENDC}")

def print_next_steps() -> None:
    """Print the next steps for development."""
    print_header("Next Steps")
    
    steps = [
        "1. Start the backend server: python -m uvicorn src.server.main:app --reload --port 8000",
        "2. Start the frontend: cd hero-foundry && npm run dev",
        "3. Start the desktop app: cd hero-foundry && npm run tauri:dev",
        "4. Access the API documentation: http://localhost:8000/docs",
        "5. Test the database connection using the provided scripts"
    ]
    
    for step in steps:
        print(f"  {step}")
    
    print(f"\n{Colors.BOLD}Happy coding! 🎲⚔️✨{Colors.ENDC}")

def main():
    """Main setup function."""
    print_header("The Hero Foundry - Development Environment Setup")
    
    # Check prerequisites
    print_header("Checking Prerequisites")
    
    if not all([
        check_python_version(),
        check_docker(),
        check_docker_compose(),
        check_node_version()
    ]):
        print_error("Prerequisites check failed. Please install required software.")
        sys.exit(1)
    
    # Create project directories
    print_header("Setting Up Project Structure")
    create_directories()
    
    # Start database services
    print_header("Starting Database Services")
    if not start_database_services():
        print_error("Failed to start database services")
        sys.exit(1)
    
    # Test database connections
    print_header("Testing Database Connections")
    if not test_database_connection():
        print_error("Database connection test failed")
        sys.exit(1)
    
    # Initialize database
    print_header("Initializing Database")
    if not initialize_database():
        print_warning("Database initialization had issues, but continuing...")
    
    # Start optional services
    print_header("Starting Optional Services")
    start_optional_services()
    
    # Setup development environments
    print_header("Setting Up Development Environments")
    setup_python_environment()
    setup_node_environment()
    
    # Print service information
    print_service_urls()
    
    # Print next steps
    print_next_steps()
    
    print_success("Development environment setup completed!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Setup failed: {e}")
        sys.exit(1)
