#!/bin/bash

# The Hero Foundry - Project Setup Script
# This script initializes the development environment for The Hero Foundry project

set -e

echo "🚀 The Hero Foundry - Project Setup"
echo "====================================="

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

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d ".bmad-core" ]; then
    print_error "This script must be run from the project root directory"
    exit 1
fi

print_status "Setting up The Hero Foundry development environment..."

# Create source code directories
print_status "Creating source code structure..."
mkdir -p src/hero_foundry/{core,models,services,api/routes,utils,tasks,migrations}
mkdir -p src/hero_foundry/api/graphql/resolvers
mkdir -p tests/{unit,integration,e2e}
mkdir -p frontend/src/{components,pages,hooks,services,store,types,utils,styles}
mkdir -p frontend/public/assets/{images,icons,fonts}
mkdir -p scripts/utils
mkdir -p docker/{nginx,postgres}
mkdir -p .github/workflows

print_success "Directory structure created"

# Create Python package files
print_status "Setting up Python package structure..."
touch src/hero_foundry/__init__.py
touch src/hero_foundry/core/__init__.py
touch src/hero_foundry/models/__init__.py
touch src/hero_foundry/services/__init__.py
touch src/hero_foundry/api/__init__.py
touch src/hero_foundry/api/routes/__init__.py
touch src/hero_foundry/api/graphql/__init__.py
touch src/hero_foundry/api/graphql/resolvers/__init__.py
touch src/hero_foundry/utils/__init__.py
touch src/hero_foundry/tasks/__init__.py
touch src/hero_foundry/migrations/__init__.py

print_success "Python package structure created"

# Create test package files
print_status "Setting up test structure..."
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py
touch tests/e2e/__init__.py

print_success "Test structure created"

# Create frontend package files
print_status "Setting up frontend structure..."
touch frontend/src/components/{common,layout,hero,story,quest,user,team}/index.ts
touch frontend/src/pages/index.ts
touch frontend/src/hooks/index.ts
touch frontend/src/services/index.ts
touch frontend/src/store/index.ts
touch frontend/src/types/index.ts
touch frontend/src/utils/index.ts

print_success "Frontend structure created"

# Create configuration files
print_status "Creating configuration files..."

# Python configuration
cat > pyproject.toml << 'EOF'
[tool.poetry]
name = "hero-foundry"
version = "0.1.0"
description = "A comprehensive platform for creating, managing, and deploying interactive hero-based experiences"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"
packages = [{include = "hero_foundry", from = "src"}]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.104.0"
uvicorn = {extras = ["standard"], version = "^0.24.0"}
sqlalchemy = "^2.0.23"
alembic = "^1.12.1"
asyncpg = "^0.29.0"
redis = "^5.0.1"
celery = "^5.3.4"
pydantic = "^2.5.0"
python-jose = {extras = ["cryptography"], version = "^3.3.0"}
passlib = {extras = ["bcrypt"], version = "^1.7.4"}
authlib = "^1.2.1"
python-multipart = "^0.0.6"
strawberry-graphql = "^0.215.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.3"
pytest-asyncio = "^0.21.1"
pytest-cov = "^4.1.0"
pytest-httpx = "^0.25.2"
pytest-mock = "^3.12.0"
pytest-postgresql = "^4.1.4"
black = "^23.11.0"
isort = "^5.12.0"
flake8 = "^6.1.0"
mypy = "^1.7.1"
bandit = "^1.7.5"
pre-commit = "^3.5.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 88
target-version = ['py311']

[tool.isort]
profile = "black"
multi_line_output = 3

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
EOF

# Requirements file for pip users
cat > requirements.txt << 'EOF'
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.23
alembic>=1.12.1
asyncpg>=0.29.0
redis>=5.0.1
celery>=5.3.4
pydantic>=2.5.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
authlib>=1.2.1
python-multipart>=0.0.6
strawberry-graphql>=0.215.0
EOF

# Development requirements
cat > requirements-dev.txt << 'EOF'
-r requirements.txt
pytest>=7.4.3
pytest-asyncio>=0.21.1
pytest-cov>=4.1.0
pytest-httpx>=0.25.2
pytest-mock>=3.12.0
pytest-postgresql>=4.1.4
black>=23.11.0
isort>=5.12.0
flake8>=6.1.0
mypy>=1.7.1
bandit>=1.7.5
pre-commit>=3.5.0
EOF

print_success "Python configuration files created"

# Frontend configuration
cat > frontend/package.json << 'EOF'
{
  "name": "hero-foundry-frontend",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint": "eslint src --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "lint:fix": "eslint src --ext ts,tsx --fix",
    "format": "prettier --write src/**/*.{ts,tsx,css,md}"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "typescript": "^5.0.0",
    "zustand": "^4.4.0",
    "@tanstack/react-query": "^4.29.0",
    "@mui/material": "^5.14.0",
    "@emotion/react": "^11.11.0",
    "@emotion/styled": "^11.11.0",
    "react-hook-form": "^7.45.0",
    "zod": "^3.22.0",
    "lucide-react": "^0.263.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.0.0",
    "vite": "^4.4.0",
    "jest": "^29.5.0",
    "@testing-library/react": "^13.4.0",
    "@testing-library/jest-dom": "^5.16.5",
    "cypress": "^12.17.0",
    "msw": "^1.2.0"
  }
}
EOF

print_success "Frontend configuration created"

# Docker configuration
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: hero_foundry
      POSTGRES_USER: hero_user
      POSTGRES_PASSWORD: hero_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U hero_user -d hero_foundry"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:
EOF

print_success "Docker configuration created"

# Environment file template
cat > .env.example << 'EOF'
# Database Configuration
DATABASE_URL=postgresql+asyncpg://hero_user:hero_password@localhost:5432/hero_foundry
DATABASE_TEST_URL=postgresql+asyncpg://hero_user:hero_password@localhost:5432/hero_foundry_test

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Application Settings
DEBUG=true
ENVIRONMENT=development
API_V1_STR=/api/v1
PROJECT_NAME=The Hero Foundry

# CORS Settings
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]

# File Storage
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760  # 10MB
EOF

print_success "Environment configuration template created"

# Git ignore file
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/
env.bak/
venv.bak/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/

# Database
*.db
*.sqlite3

# Coverage reports
htmlcov/
.coverage
.coverage.*
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Frontend build
frontend/dist/
frontend/build/

# Docker
.dockerignore

# AI development
.ai/debug-log.md
.ai/development-notes.md

# Temporary files
*.tmp
*.temp
EOF

print_success "Git ignore file created"

# Pre-commit configuration
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3.11
        args: [--line-length=88]

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: [--profile=black]

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203,W503]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--ignore-missing-imports]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [-r, src/, -f, json, -o, bandit-report.json]
EOF

print_success "Pre-commit configuration created"

# Make setup script executable
chmod +x scripts/setup.sh

print_success "Setup script completed successfully!"
echo ""
echo "🎉 The Hero Foundry project is now ready for development!"
echo ""
echo "📋 Next steps:"
echo "1. Create a Python virtual environment: python -m venv venv"
echo "2. Activate the virtual environment: source venv/bin/activate (or venv\\Scripts\\activate on Windows)"
echo "3. Install Python dependencies: pip install -r requirements.txt"
echo "4. Start the database: docker-compose up -d"
echo "5. Set up your environment variables: cp .env.example .env"
echo "6. Begin development with your preferred IDE!"
echo ""
echo "🔧 BMAD methodology is fully integrated and ready to use"
echo "📚 Check the docs/ directory for comprehensive documentation"
echo "🚀 Happy coding!"




