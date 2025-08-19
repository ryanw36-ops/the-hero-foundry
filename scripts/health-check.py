#!/usr/bin/env python3
"""
The Hero Foundry - Development Environment Health Check
======================================================

This script performs a comprehensive health check of the development environment,
including Docker services, database connections, and application readiness.

Usage:
    python scripts/health-check.py
"""

import os
import sys
import subprocess
import time
import json
import platform
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

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

class HealthCheckResult:
    """Class to store health check results."""
    
    def __init__(self, name: str):
        self.name = name
        self.status = "unknown"
        self.message = ""
        self.details = {}
        self.timestamp = datetime.now()
    
    def set_success(self, message: str, details: Dict = None):
        """Set the result as successful."""
        self.status = "success"
        self.message = message
        self.details = details or {}
    
    def set_warning(self, message: str, details: Dict = None):
        """Set the result as warning."""
        self.status = "warning"
        self.message = message
        self.details = details or {}
    
    def set_error(self, message: str, details: Dict = None):
        """Set the result as error."""
        self.status = "error"
        self.message = message
        self.details = details or {}
    
    def __str__(self):
        status_colors = {
            "success": Colors.OKGREEN,
            "warning": Colors.WARNING,
            "error": Colors.FAIL,
            "unknown": Colors.OKBLUE
        }
        color = status_colors.get(self.status, Colors.OKBLUE)
        return f"{color}[{self.status.upper()}]{Colors.ENDC} {self.name}: {self.message}"

def check_docker_services() -> List[HealthCheckResult]:
    """Check the status of Docker services."""
    print_status("Checking Docker services...")
    results = []
    
    try:
        # Check if docker-compose.dev.yml exists
        compose_file = Path("docker-compose.dev.yml")
        if not compose_file.exists():
            result = HealthCheckResult("Docker Compose File")
            result.set_error("docker-compose.dev.yml not found")
            results.append(result)
            return results
        
        # Get service status
        cmd = ["docker-compose", "-f", "docker-compose.dev.yml", "ps", "--format", "json"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        services = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                try:
                    service_info = json.loads(line)
                    services.append(service_info)
                except json.JSONDecodeError:
                    continue
        
        # Check each service
        expected_services = ["postgres", "redis"]
        optional_services = ["pgadmin", "redis-commander", "mailhog"]
        
        for service_name in expected_services:
            result = HealthCheckResult(f"Service: {service_name}")
            service = next((s for s in services if s.get('Service') == service_name), None)
            
            if service:
                if service.get('State') == 'Up':
                    result.set_success(f"Service is running", {
                        "container_id": service.get('ID', 'unknown'),
                        "ports": service.get('Ports', 'unknown')
                    })
                else:
                    result.set_error(f"Service is not running (State: {service.get('State', 'unknown')}")
            else:
                result.set_error("Service not found")
            
            results.append(result)
        
        # Check optional services
        for service_name in optional_services:
            result = HealthCheckResult(f"Optional Service: {service_name}")
            service = next((s for s in services if s.get('Service') == service_name), None)
            
            if service:
                if service.get('State') == 'Up':
                    result.set_success(f"Service is running", {
                        "container_id": service.get('ID', 'unknown'),
                        "ports": service.get('Ports', 'unknown')
                    })
                else:
                    result.set_warning(f"Service is not running (State: {service.get('State', 'unknown')}")
            else:
                result.set_warning("Service not found (optional)")
            
            results.append(result)
        
    except subprocess.CalledProcessError as e:
        result = HealthCheckResult("Docker Services")
        result.set_error(f"Failed to check Docker services: {e}")
        results.append(result)
    
    return results

def check_database_connections() -> List[HealthCheckResult]:
    """Check database connections."""
    print_status("Checking database connections...")
    results = []
    
    # Check PostgreSQL connection
    try:
        cmd = [
            "docker-compose", "-f", "docker-compose.dev.yml", "exec", "-T", "postgres",
            "pg_isready", "-U", "hero_foundry", "-d", "hero_foundry"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        db_result = HealthCheckResult("PostgreSQL Connection")
        if 'accepting connections' in result.stdout:
            db_result.set_success("Database is accepting connections")
        else:
            db_result.set_error("Database is not accepting connections")
        results.append(db_result)
        
    except subprocess.CalledProcessError as e:
        db_result = HealthCheckResult("PostgreSQL Connection")
        db_result.set_error(f"Connection failed: {e}")
        results.append(db_result)
    
    # Check Redis connection
    try:
        cmd = [
            "docker-compose", "-f", "docker-compose.dev.yml", "exec", "-T", "redis",
            "redis-cli", "ping"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        redis_result = HealthCheckResult("Redis Connection")
        if 'PONG' in result.stdout:
            redis_result.set_success("Redis is responding")
        else:
            redis_result.set_error("Redis is not responding")
        results.append(redis_result)
        
    except subprocess.CalledProcessError as e:
        redis_result = HealthCheckResult("Redis Connection")
        redis_result.set_error(f"Connection failed: {e}")
        results.append(redis_result)
    
    return results

def check_database_schema() -> List[HealthCheckResult]:
    """Check database schema and data."""
    print_status("Checking database schema...")
    results = []
    
    try:
        # Check if tables exist
        cmd = [
            "docker-compose", "-f", "docker-compose.dev.yml", "exec", "-T", "postgres",
            "psql", "-U", "hero_foundry", "-d", "hero_foundry", "-t", "-c",
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        tables = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        expected_tables = ["rulesets", "characters", "character_snapshots", "homebrew_content", "ai_chat_sessions"]
        
        schema_result = HealthCheckResult("Database Schema")
        missing_tables = [table for table in expected_tables if table not in tables]
        
        if not missing_tables:
            schema_result.set_success(f"All expected tables found ({len(tables)} total)", {
                "tables": tables,
                "expected_count": len(expected_tables)
            })
        else:
            schema_result.set_warning(f"Missing tables: {missing_tables}", {
                "found_tables": tables,
                "missing_tables": missing_tables
            })
        
        results.append(schema_result)
        
        # Check if default ruleset exists
        cmd = [
            "docker-compose", "-f", "docker-compose.dev.yml", "exec", "-T", "postgres",
            "psql", "-U", "hero_foundry", "-d", "hero_foundry", "-t", "-c",
            "SELECT COUNT(*) FROM rulesets WHERE id = 'dnd5e';"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        ruleset_result = HealthCheckResult("Default Ruleset")
        count = int(result.stdout.strip())
        
        if count > 0:
            ruleset_result.set_success("Default D&D 5e ruleset found")
        else:
            ruleset_result.set_warning("Default ruleset not found")
        
        results.append(ruleset_result)
        
    except subprocess.CalledProcessError as e:
        schema_result = HealthCheckResult("Database Schema")
        schema_result.set_error(f"Failed to check schema: {e}")
        results.append(schema_result)
    
    return results

def check_development_environment() -> List[HealthCheckResult]:
    """Check development environment setup."""
    print_status("Checking development environment...")
    results = []
    
    # Check Python virtual environment
    venv_result = HealthCheckResult("Python Virtual Environment")
    venv_path = Path(".venv")
    
    if venv_path.exists():
        if platform.system() == "Windows":
            python_path = venv_path / "Scripts" / "python.exe"
        else:
            python_path = venv_path / "bin" / "python"
        
        if python_path.exists():
            venv_result.set_success("Virtual environment exists and is accessible")
        else:
            venv_result.set_warning("Virtual environment exists but Python not found")
    else:
        venv_result.set_warning("Virtual environment not found")
    
    results.append(venv_result)
    
    # Check requirements.txt
    req_result = HealthCheckResult("Python Requirements")
    req_path = Path("requirements.txt")
    
    if req_path.exists():
        req_result.set_success("requirements.txt found")
    else:
        req_result.set_warning("requirements.txt not found")
    
    results.append(req_result)
    
    # Check Node.js environment
    node_result = HealthCheckResult("Node.js Environment")
    package_path = Path("hero-foundry/package.json")
    
    if package_path.exists():
        node_result.set_success("package.json found in hero-foundry directory")
    else:
        node_result.set_warning("package.json not found in hero-foundry directory")
    
    results.append(node_result)
    
    # Check project directories
    dir_result = HealthCheckResult("Project Directories")
    expected_dirs = ["storage", "content", "exports", "logs"]
    existing_dirs = []
    missing_dirs = []
    
    for directory in expected_dirs:
        if Path(directory).exists():
            existing_dirs.append(directory)
        else:
            missing_dirs.append(directory)
    
    if not missing_dirs:
        dir_result.set_success("All project directories exist")
    else:
        dir_result.set_warning(f"Missing directories: {missing_dirs}")
    
    dir_result.details = {
        "existing": existing_dirs,
        "missing": missing_dirs
    }
    results.append(dir_result)
    
    return results

def check_network_ports() -> List[HealthCheckResult]:
    """Check if expected network ports are accessible."""
    print_status("Checking network ports...")
    results = []
    
    import socket
    
    expected_ports = {
        5432: "PostgreSQL",
        6379: "Redis",
        5050: "pgAdmin",
        8081: "Redis Commander",
        8025: "MailHog"
    }
    
    for port, service in expected_ports.items():
        result = HealthCheckResult(f"Port {port} ({service})")
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result_socket = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result_socket == 0:
                result.set_success(f"Port {port} is accessible")
            else:
                result.set_warning(f"Port {port} is not accessible")
        except Exception as e:
            result.set_error(f"Failed to check port {port}: {e}")
        
        results.append(result)
    
    return results

def print_summary(all_results: List[HealthCheckResult]):
    """Print a summary of all health check results."""
    print_header("Health Check Summary")
    
    # Count results by status
    status_counts = {}
    for result in all_results:
        status = result.status
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Print summary
    total = len(all_results)
    success_count = status_counts.get('success', 0)
    warning_count = status_counts.get('warning', 0)
    error_count = status_counts.get('error', 0)
    
    print(f"Total Checks: {total}")
    print(f"{Colors.OKGREEN}Successful: {success_count}{Colors.ENDC}")
    print(f"{Colors.WARNING}Warnings: {warning_count}{Colors.ENDC}")
    print(f"{Colors.FAIL}Errors: {error_count}{Colors.ENDC}")
    
    # Calculate health percentage
    if total > 0:
        health_percentage = (success_count / total) * 100
        if health_percentage >= 90:
            health_status = f"{Colors.OKGREEN}Excellent{Colors.ENDC}"
        elif health_percentage >= 75:
            health_status = f"{Colors.OKCYAN}Good{Colors.ENDC}"
        elif health_percentage >= 50:
            health_status = f"{Colors.WARNING}Fair{Colors.ENDC}"
        else:
            health_status = f"{Colors.FAIL}Poor{Colors.ENDC}"
        
        print(f"\nOverall Health: {health_percentage:.1f}% - {health_status}")
    
    # Print detailed results
    print_header("Detailed Results")
    for result in all_results:
        print(f"  {result}")
        if result.details:
            for key, value in result.details.items():
                print(f"    {key}: {value}")

def main():
    """Main health check function."""
    print_header("The Hero Foundry - Development Environment Health Check")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Platform: {platform.system()} {platform.release()}")
    
    all_results = []
    
    # Run all health checks
    checks = [
        ("Docker Services", check_docker_services),
        ("Database Connections", check_database_connections),
        ("Database Schema", check_database_schema),
        ("Development Environment", check_development_environment),
        ("Network Ports", check_network_ports)
    ]
    
    for check_name, check_function in checks:
        print_header(f"Checking {check_name}")
        try:
            results = check_function()
            all_results.extend(results)
            
            # Print immediate results
            for result in results:
                print(f"  {result}")
                
        except Exception as e:
            error_result = HealthCheckResult(check_name)
            error_result.set_error(f"Health check failed: {e}")
            all_results.append(error_result)
            print(f"  {error_result}")
    
    # Print summary
    print_summary(all_results)
    
    # Print recommendations
    print_header("Recommendations")
    
    error_count = sum(1 for r in all_results if r.status == 'error')
    warning_count = sum(1 for r in all_results if r.status == 'warning')
    
    if error_count == 0 and warning_count == 0:
        print_success("Your development environment is healthy and ready for development!")
        print("You can now start building The Hero Foundry!")
    elif error_count == 0:
        print_warning("Your environment has some warnings but should work for development.")
        print("Consider addressing the warnings for optimal performance.")
    else:
        print_error("Your environment has errors that need to be fixed before development.")
        print("Please address the errors above and run this health check again.")
    
    print(f"\n{Colors.BOLD}Happy coding! 🎲⚔️✨{Colors.ENDC}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nHealth check interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Health check failed: {e}")
        sys.exit(1)
