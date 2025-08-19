# Technology Stack - The Hero Foundry

## Overview
This document outlines the complete technology stack for The Hero Foundry project, including all frameworks, libraries, tools, and infrastructure components.

## Backend Technology Stack

### Core Runtime & Framework
- **Python Version:** 3.11+ (as per project requirements)
- **Framework:** FastAPI 0.104+ - High-performance, modern web framework
- **ASGI Server:** Uvicorn - Lightning-fast ASGI server implementation
- **Type Checking:** Pydantic 2.0+ - Data validation using Python type annotations

### Database & ORM
- **Primary Database:** PostgreSQL 15+ - Advanced open-source relational database
- **ORM:** SQLAlchemy 2.0+ - Modern Python SQL toolkit and ORM
- **Database Migrations:** Alembic - Database migration tool for SQLAlchemy
- **Connection Pooling:** asyncpg - Fast PostgreSQL driver for async/await
- **Redis:** 7.0+ - In-memory data structure store for caching and sessions

### Authentication & Security
- **JWT Library:** python-jose[cryptography] - JavaScript Object Signing and Encryption
- **Password Hashing:** passlib[bcrypt] - Password hashing library
- **OAuth:** authlib - Python authentication library
- **Security Headers:** secure - Security headers middleware
- **Rate Limiting:** slowapi - Rate limiting for FastAPI

### Background Tasks & Queues
- **Task Queue:** Celery 5.3+ - Distributed task queue
- **Message Broker:** Redis - Message broker for Celery
- **Result Backend:** Redis - Store task results
- **Monitoring:** Flower - Web-based monitoring for Celery

### API & Serialization
- **API Documentation:** OpenAPI 3.0+ (FastAPI auto-generates)
- **GraphQL:** Strawberry GraphQL - Modern GraphQL library for Python
- **Serialization:** Pydantic - Data serialization and validation
- **File Uploads:** python-multipart - Streaming multipart parser

### Testing Framework
- **Testing:** pytest 7.4+ - Testing framework
- **Async Testing:** pytest-asyncio - Async support for pytest
- **Coverage:** pytest-cov - Coverage reporting plugin
- **HTTP Testing:** pytest-httpx - HTTP testing for pytest
- **Mocking:** pytest-mock - Mocking plugin for pytest
- **Database Testing:** pytest-postgresql - PostgreSQL testing fixtures

### Development Tools
- **Code Formatting:** Black 23.3+ - Uncompromising code formatter
- **Import Sorting:** isort 5.12+ - Import statement sorting
- **Linting:** flake8 6.0+ - Style guide enforcement
- **Type Checking:** mypy 1.5+ - Static type checker
- **Security Scanning:** bandit 1.7+ - Security linter
- **Pre-commit Hooks:** pre-commit - Git hooks framework

## Frontend Technology Stack

### Core Framework
- **Framework:** React 18+ - JavaScript library for building user interfaces
- **Language:** TypeScript 5.0+ - Typed superset of JavaScript
- **Build Tool:** Vite 4.4+ - Next generation frontend tooling
- **Package Manager:** npm 9.0+ or yarn 1.22+ - Package management

### State Management
- **State Library:** Zustand 4.4+ - Small, fast and scalable state management
- **Alternative:** Redux Toolkit 1.9+ - Official Redux logic and tooling
- **Server State:** TanStack Query 4.29+ - Powerful data synchronization

### UI Components & Styling
- **Component Library:** Material-UI (MUI) 5.14+ - React component library
- **Alternative:** Chakra UI 2.8+ - Simple, modular and accessible component library
- **Styling:** Emotion 11.11+ - CSS-in-JS library
- **Icons:** Lucide React 0.263+ - Beautiful & consistent icon toolkit

### Routing & Navigation
- **Router:** React Router 6.8+ - Declarative routing for React
- **Navigation:** React Navigation 6.1+ (for mobile) - Navigation library

### Forms & Validation
- **Form Library:** React Hook Form 7.45+ - Performant forms with minimal re-renders
- **Validation:** Zod 3.22+ - TypeScript-first schema validation
- **Alternative:** Yup 1.3+ - JavaScript schema builder for value parsing

### Testing
- **Testing Framework:** Jest 29.5+ - JavaScript testing framework
- **Component Testing:** React Testing Library 13.4+ - Testing utilities for React
- **E2E Testing:** Cypress 12.17+ - End-to-end testing framework
- **Mocking:** MSW 1.2+ - API mocking library

## Infrastructure & DevOps

### Containerization
- **Container Engine:** Docker 24.0+ - Container platform
- **Container Orchestration:** Docker Compose 2.20+ - Multi-container applications
- **Production:** Kubernetes 1.28+ - Container orchestration platform

### CI/CD Pipeline
- **Version Control:** Git 2.40+ - Distributed version control
- **CI/CD Platform:** GitHub Actions - Automated workflows
- **Alternative:** GitLab CI/CD - GitLab's continuous integration
- **Artifact Storage:** GitHub Packages - Package registry

### Monitoring & Observability
- **Application Monitoring:** Prometheus 2.45+ - Monitoring system
- **Visualization:** Grafana 10.0+ - Analytics and monitoring platform
- **Logging:** ELK Stack (Elasticsearch, Logstash, Kibana)
- **Tracing:** OpenTelemetry - Observability framework
- **Health Checks:** Healthcheck - Health check endpoint

### Cloud & Hosting
- **Cloud Platform:** AWS, Azure, or Google Cloud Platform
- **Container Registry:** Docker Hub, AWS ECR, or Azure Container Registry
- **CDN:** CloudFront, Azure CDN, or Cloud CDN
- **Database Hosting:** Managed PostgreSQL services (RDS, Azure Database, Cloud SQL)

## Development Environment

### Local Development
- **Python Environment:** pyenv + virtualenv or conda
- **Node Environment:** nvm or fnm for Node.js version management
- **Database:** Docker containers for PostgreSQL and Redis
- **IDE Support:** VS Code, PyCharm, or Cursor with appropriate extensions

### Code Quality Tools
- **Pre-commit Hooks:** Automated code quality checks
- **Editor Config:** Consistent coding style across editors
- **ESLint Config:** JavaScript/TypeScript linting rules
- **Prettier Config:** Code formatting configuration

## Dependencies & Versions

### Python Dependencies
```toml
# pyproject.toml
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
```

### Node.js Dependencies
```json
{
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
```

## Version Compatibility Matrix

### Python Compatibility
- **Python 3.11:** Full support, recommended for development
- **Python 3.12:** Full support, latest features
- **Python 3.10:** Limited support, some features may not work
- **Python 3.9 and below:** Not supported

### Node.js Compatibility
- **Node.js 18:** Full support, LTS version
- **Node.js 20:** Full support, current LTS version
- **Node.js 16:** Limited support, end of life
- **Node.js 14 and below:** Not supported

### Browser Compatibility
- **Chrome 90+:** Full support
- **Firefox 88+:** Full support
- **Safari 14+:** Full support
- **Edge 90+:** Full support
- **Internet Explorer:** Not supported

## Migration & Upgrade Paths

### Python Dependencies
- **FastAPI:** Upgrade path from 0.95+ to 0.104+
- **SQLAlchemy:** Major upgrade from 1.4 to 2.0 requires code changes
- **Pydantic:** Major upgrade from 1.x to 2.x requires code changes

### Frontend Dependencies
- **React:** Upgrade path from 17 to 18 (concurrent features)
- **TypeScript:** Upgrade path from 4.x to 5.x (new features)
- **Material-UI:** Upgrade path from 4.x to 5.x (new components)

## Security Considerations

### Dependency Security
- **Regular Updates:** Monthly dependency updates
- **Security Scanning:** Automated vulnerability scanning
- **License Compliance:** Regular license compliance checks
- **Supply Chain Security:** Verify package integrity

### Runtime Security
- **Container Security:** Regular base image updates
- **Network Security:** Proper firewall and network segmentation
- **Access Control:** Principle of least privilege
- **Monitoring:** Security event monitoring and alerting

---

*This technology stack provides a modern, scalable foundation for The Hero Foundry project. All versions and dependencies are regularly updated to maintain security and performance.*




