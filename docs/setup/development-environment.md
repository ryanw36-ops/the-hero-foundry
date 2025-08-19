# Development Environment Setup Guide

## 🚀 Quick Start (30 Minutes or Less)

This guide will get you up and running with The Hero Foundry development environment in under 30 minutes. Follow the steps below to set up your local development environment.

## 📋 Prerequisites

### Required Tools & Versions

| Tool | Version | Purpose | Download |
|------|---------|---------|----------|
| **Python** | 3.11.x | Backend services, AI integration | [python.org](https://www.python.org/downloads/) |
| **Node.js** | 18.x LTS | Frontend development, package management | [nodejs.org](https://nodejs.org/) |
| **Git** | 2.40+ | Version control | [git-scm.com](https://git-scm.com/) |
| **Docker Desktop** | 4.20+ | Local services (PostgreSQL, Redis) | [docker.com](https://www.docker.com/products/docker-desktop/) |
| **VS Code / Cursor** | Latest | Recommended IDE | [cursor.sh](https://cursor.sh/) |

### System Requirements

- **OS**: Windows 10/11, macOS 12+, or Ubuntu 20.04+
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 2GB free space
- **Network**: Internet connection for initial setup

## 🛠️ Step-by-Step Setup

### 1. Clone the Repository

```bash
# Clone the repository
git clone <repository-url>
cd the-hero-foundry

# Verify you're in the correct directory
ls -la
# Should show: .bmad-core/, docs/, requirements.txt, docker-compose.yml, etc.
```

### 2. Install Python Dependencies

```bash
# Create and activate Python virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Verify Python version (must be 3.11.x)
python --version

# Install Python dependencies
pip install -r requirements.txt

# Verify installation
python -c "import fastapi, uvicorn, sqlalchemy; print('✅ Python dependencies installed successfully')"
```

### 3. Install Node.js Dependencies

```bash
# Verify Node.js version (must be 18.x)
node --version
npm --version

# Install Node.js dependencies
npm install

# Verify installation
npm run --silent
```

### 4. Start Local Services with Docker

```bash
# Start PostgreSQL and Redis services
docker-compose up -d postgres redis

# Wait for services to be ready (check with)
docker-compose ps

# Verify database connection
python scripts/test-database-connection.py
```

### 5. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
# Use your preferred editor (VS Code, nano, vim, etc.)
code .env
```

**Required Environment Variables:**

```bash
# Database Configuration
DATABASE_URL=postgresql://hero_foundry:password@localhost:5432/hero_foundry
REDIS_URL=redis://localhost:6379

# AI Provider (Optional for development)
AI_PROVIDER_API_KEY=your_api_key_here

# Application Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
DEBUG=true

# Server Configuration
BACKEND_PORT=8000
FRONTEND_PORT=3000
```

### 6. Database Setup

```bash
# Run database migrations
python scripts/setup_database.py

# Load sample data (optional)
python scripts/load_sample_data.py

# Verify database setup
python scripts/verify_database.py
```

### 7. Start Development Servers

```bash
# Terminal 1: Start Backend (FastAPI)
npm run dev:backend
# or manually:
# cd apps/backend
# python -m uvicorn src.main:app --reload --port 8000

# Terminal 2: Start Frontend (React)
npm run dev:frontend
# or manually:
# cd apps/frontend
# npm start

# Terminal 3: Start Desktop App (Electron)
npm run dev:desktop
```

## 🔧 Development Server Configuration

### Backend Server (FastAPI)

- **URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Frontend Server (React)

- **URL**: http://localhost:3000
- **Hot Reload**: Enabled by default
- **Build Tool**: Vite with HMR

### Desktop App (Electron)

- **Development Mode**: Hot reload enabled
- **DevTools**: Accessible via F12 or Ctrl+Shift+I
- **Console**: View logs in DevTools Console

## 🗄️ Database Configuration

### PostgreSQL Setup

```yaml
# docker-compose.yml excerpt
services:
  postgres:
    image: postgres:15-alpine
    container_name: hero-foundry-postgres
    environment:
      POSTGRES_DB: hero_foundry
      POSTGRES_USER: hero_foundry
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U hero_foundry"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### Redis Setup

```yaml
# docker-compose.yml excerpt
services:
  redis:
    image: redis:7-alpine
    container_name: hero-foundry-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
```

## 🧪 Testing Setup

### Running Tests

```bash
# Run all tests
npm run test

# Run specific test suites
npm run test:backend      # Python backend tests
npm run test:frontend     # React frontend tests
npm run test:e2e          # End-to-end tests

# Run tests with coverage
npm run test:coverage

# Run tests in watch mode
npm run test:watch
```

### Test Configuration

```bash
# Backend testing (pytest)
pytest tests/ -v --cov=src --cov-report=html

# Frontend testing (Vitest)
npm run test:frontend -- --coverage

# E2E testing (Playwright)
npx playwright test --headed
```

## 🔍 Development Tools

### Code Quality Tools

```bash
# Python code formatting and linting
black src/ tests/
flake8 src/ tests/
isort src/ tests/

# Type checking
mypy src/

# Frontend code formatting
npm run lint
npm run format
```

### Database Tools

```bash
# Database management
python scripts/db-shell.py

# Migration management
python scripts/manage-migrations.py

# Data export/import
python scripts/export-data.py
python scripts/import-data.py
```

## 🚨 Troubleshooting

### Common Issues & Solutions

#### Python Virtual Environment Issues

```bash
# If virtual environment activation fails
python -m venv .venv --clear
# On Windows, ensure PowerShell execution policy allows scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check database logs
docker-compose logs postgres

# Reset database (WARNING: This will delete all data)
docker-compose down -v
docker-compose up -d postgres redis
```

#### Port Conflicts

```bash
# Check what's using port 8000
# On Windows:
netstat -ano | findstr :8000
# On macOS/Linux:
lsof -i :8000

# Kill process if needed
# On Windows:
taskkill /PID <PID> /F
# On macOS/Linux:
kill -9 <PID>
```

#### Node.js Dependencies Issues

```bash
# Clear npm cache
npm cache clean --force

# Remove node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Performance Optimization

```bash
# Enable Python performance optimizations
export PYTHONOPTIMIZE=1

# Use faster Python package manager (optional)
pip install uv
uv sync

# Enable Node.js optimizations
export NODE_OPTIONS="--max-old-space-size=4096"
```

## 📚 Additional Resources

### Documentation

- [Project Architecture](./../fullstack-architecture.md)
- [API Documentation](http://localhost:8000/docs)
- [Frontend Component Library](./../frontend/components.md)

### Development Workflow

- [Git Workflow](./../git-workflow.md)
- [Code Review Guidelines](./../code-review.md)
- [Deployment Guide](./../deployment.md)

### External Tools

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Electron Documentation](https://www.electronjs.org/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## ✅ Verification Checklist

Before starting development, ensure all items are checked:

- [ ] Python 3.11.x installed and virtual environment activated
- [ ] Node.js 18.x installed and npm working
- [ ] Docker Desktop running with PostgreSQL and Redis containers
- [ ] Environment variables configured in `.env` file
- [ ] Database migrations completed successfully
- [ ] Backend server running on http://localhost:8000
- [ ] Frontend server running on http://localhost:3000
- [ ] All tests passing (`npm run test`)
- [ ] API documentation accessible at http://localhost:8000/docs

## 🆘 Getting Help

If you encounter issues not covered in this guide:

1. **Check the logs**: Look at terminal output and Docker logs
2. **Search issues**: Check existing GitHub issues
3. **Ask the team**: Reach out to the development team
4. **Document the issue**: Help others by documenting new solutions

## 🎯 Next Steps

Once your development environment is set up:

1. **Explore the codebase**: Familiarize yourself with the project structure
2. **Run the application**: Create a test character to verify everything works
3. **Read the architecture docs**: Understand the system design
4. **Pick up a task**: Start contributing to the project

---

**Happy coding! 🎲⚔️✨**

*This guide is maintained by the development team. If you find any issues or have suggestions for improvements, please submit a pull request or create an issue.*
