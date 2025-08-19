#!/usr/bin/env python3
"""
The Hero Foundry - Quick Start Script
=====================================

This script provides quick access to common development tasks and commands.
It's designed to help developers get up and running quickly.

Usage:
    python scripts/quick-start.py [command]

Commands:
    start       - Start all development services
    stop        - Stop all development services
    restart     - Restart all development services
    status      - Show service status
    logs        - Show service logs
    health      - Run health check
    setup       - Run full setup
    help        - Show this help message
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

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

def check_docker_compose_file():
    """Check if docker-compose.dev.yml exists."""
    compose_file = Path("docker-compose.dev.yml")
    if not compose_file.exists():
        print_error("docker-compose.dev.yml not found")
        print_error("Please run this script from the project root directory")
        return False
    return True

def start_services():
    """Start all development services."""
    print_header("Starting Development Services")
    
    if not check_docker_compose_file():
        return False
    
    try:
        # Start core services
        print_status("Starting core services (PostgreSQL, Redis)...")
        subprocess.run([
            "docker-compose", "-f", "docker-compose.dev.yml", "up", "-d", "postgres", "redis"
        ], check=True)
        
        # Wait a moment for services to start
        import time
        time.sleep(5)
        
        # Start optional services
        print_status("Starting optional services (pgAdmin, Redis Commander, MailHog)...")
        subprocess.run([
            "docker-compose", "-f", "docker-compose.dev.yml", "--profile", "tools", "up", "-d"
        ], check=True)
        
        print_success("All services started successfully!")
        print_status("Services are starting up, please wait a moment before using them")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to start services: {e}")
        return False

def stop_services():
    """Stop all development services."""
    print_header("Stopping Development Services")
    
    if not check_docker_compose_file():
        return False
    
    try:
        print_status("Stopping all services...")
        subprocess.run([
            "docker-compose", "-f", "docker-compose.dev.yml", "down"
        ], check=True)
        
        print_success("All services stopped successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to stop services: {e}")
        return False

def restart_services():
    """Restart all development services."""
    print_header("Restarting Development Services")
    
    if stop_services():
        import time
        time.sleep(2)
        return start_services()
    return False

def show_status():
    """Show the status of all services."""
    print_header("Service Status")
    
    if not check_docker_compose_file():
        return False
    
    try:
        print_status("Checking service status...")
        subprocess.run([
            "docker-compose", "-f", "docker-compose.dev.yml", "ps"
        ], check=True)
        
        print_status("Service URLs:")
        print("  PostgreSQL: localhost:5432")
        print("  Redis: localhost:6379")
        print("  pgAdmin: http://localhost:5050")
        print("  Redis Commander: http://localhost:8081")
        print("  MailHog: http://localhost:8025")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to get service status: {e}")
        return False

def show_logs():
    """Show service logs."""
    print_header("Service Logs")
    
    if not check_docker_compose_file():
        return False
    
    try:
        print_status("Showing recent logs for all services...")
        subprocess.run([
            "docker-compose", "-f", "docker-compose.dev.yml", "logs", "--tail=20"
        ], check=True)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to show logs: {e}")
        return False

def run_health_check():
    """Run the health check script."""
    print_header("Running Health Check")
    
    health_script = Path("scripts/health-check.py")
    if not health_script.exists():
        print_error("Health check script not found")
        return False
    
    try:
        print_status("Running health check...")
        subprocess.run([sys.executable, str(health_script)], check=True)
        return True
        
    except subprocess.CalledProcessError as e:
        print_error(f"Health check failed: {e}")
        return False

def run_setup():
    """Run the full setup script."""
    print_header("Running Full Setup")
    
    setup_script = Path("scripts/setup-hero-foundry-dev.py")
    if not setup_script.exists():
        print_error("Setup script not found")
        return False
    
    try:
        print_status("Running full setup...")
        subprocess.run([sys.executable, str(setup_script)], check=True)
        return True
        
    except subprocess.CalledProcessError as e:
        print_error(f"Setup failed: {e}")
        return False

def show_help():
    """Show help information."""
    print_header("Quick Start Commands")
    
    commands = {
        "start": "Start all development services (PostgreSQL, Redis, pgAdmin, etc.)",
        "stop": "Stop all development services",
        "restart": "Restart all development services",
        "status": "Show the status of all services",
        "logs": "Show recent service logs",
        "health": "Run comprehensive health check",
        "setup": "Run full development environment setup",
        "help": "Show this help message"
    }
    
    for command, description in commands.items():
        print(f"  {Colors.OKCYAN}{command:<10}{Colors.ENDC} - {description}")
    
    print(f"\n{Colors.BOLD}Examples:{Colors.ENDC}")
    print(f"  python scripts/quick-start.py start")
    print(f"  python scripts/quick-start.py status")
    print(f"  python scripts/quick-start.py health")
    
    print(f"\n{Colors.BOLD}Development Workflow:{Colors.ENDC}")
    print("  1. Start services: python scripts/quick-start.py start")
    print("  2. Check status: python scripts/quick-start.py status")
    print("  3. Run health check: python scripts/quick-start.py health")
    print("  4. Start your development servers")
    print("  5. Stop services when done: python scripts/quick-start.py stop")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="The Hero Foundry - Quick Start Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/quick-start.py start
  python scripts/quick-start.py status
  python scripts/quick-start.py health
        """
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        default="help",
        choices=["start", "stop", "restart", "status", "logs", "health", "setup", "help"],
        help="Command to execute"
    )
    
    args = parser.parse_args()
    
    # Execute the requested command
    command_functions = {
        "start": start_services,
        "stop": stop_services,
        "restart": restart_services,
        "status": show_status,
        "logs": show_logs,
        "health": run_health_check,
        "setup": run_setup,
        "help": show_help
    }
    
    command_function = command_functions.get(args.command)
    if command_function:
        success = command_function()
        if success is False:
            sys.exit(1)
    else:
        print_error(f"Unknown command: {args.command}")
        show_help()
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Operation failed: {e}")
        sys.exit(1)
