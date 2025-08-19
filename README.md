# The Hero Foundry 🚀

A comprehensive platform for creating, managing, and deploying interactive hero-based experiences. Built with modern web technologies and following the BMAD methodology for agile AI-driven development.

## 🎯 Project Overview

The Hero Foundry empowers creators, developers, and storytellers to build engaging hero narratives across multiple media formats. Whether you're crafting a game character, writing a novel, or designing an interactive story, our platform provides the tools and infrastructure you need.

## ✨ Key Features

- **Hero Management System** - Create and customize heroes with comprehensive attribute systems
- **Story Builder** - Craft branching narratives and quests with intuitive tools
- **Content Creation Suite** - Support for text, images, audio, and interactive elements
- **Multi-Platform Export** - Deploy your content across web, mobile, and desktop
- **Collaboration Tools** - Work with teams on shared universes and projects
- **Analytics Dashboard** - Track engagement and optimize your content

## 🏗️ Architecture

The Hero Foundry is built with a modern, scalable architecture:

- **Backend:** FastAPI with Python 3.11+, SQLAlchemy 2.0, PostgreSQL
- **Frontend:** React 18+ with TypeScript, Material-UI, Zustand
- **Database:** PostgreSQL 15+ with Redis caching
- **Backend as a Service:** Supabase for authentication, real-time features, and storage
- **Authentication:** JWT with OAuth 2.0 support via Supabase Auth
- **Deployment:** Docker containers with Kubernetes orchestration

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose
- PostgreSQL 15+
- Redis 7.0+

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd the-hero-foundry
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Set up Supabase backend**
   ```bash
   # Follow the comprehensive setup guide
   # See: SUPABASE_SETUP.md
   ```

5. **Start development environment**
   ```bash
   docker-compose up -d
   python -m uvicorn src.hero_foundry.main:app --reload
   ```

6. **Access the application**
   - Backend API: http://localhost:8000
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/docs

## 📚 Documentation

- **[Product Requirements Document](docs/prd.md)** - Complete project specifications
- **[Architecture Guide](docs/architecture.md)** - System design and technical details
- **[API Documentation](docs/api.md)** - REST API and GraphQL endpoints
- **[Development Guide](docs/development.md)** - Contributing and development workflow
- **[Deployment Guide](docs/deployment.md)** - Production deployment instructions
- **[Supabase Setup Guide](SUPABASE_SETUP.md)** - Complete Supabase configuration guide

## 🧠 **Critical: Understanding Archon**

**Archon is the foundation of our project success.** Every team member must understand and use Archon effectively.

- **[Why Archon Matters](docs/archon-importance.md)** - **MUST READ** for all team members
- **[QA Team Job Description](docs/job-descriptions/qa-team-member.md)** - Quality assurance role and responsibilities

## 🛠️ Development

### Code Standards

- **Python:** PEP 8 compliance with Black formatter
- **TypeScript:** ESLint + Prettier configuration
- **Testing:** 90%+ code coverage requirement
- **Documentation:** Google-style docstrings

### Development Workflow

1. **Create feature branch** from `main`
2. **Implement changes** following coding standards
3. **Write tests** for new functionality
4. **Update documentation** as needed
5. **Submit pull request** for review
6. **Merge** after approval and CI checks pass

### Running Tests

```bash
# Backend tests
pytest tests/ -v --cov=src/

# Frontend tests
cd frontend
npm test

# End-to-end tests
npm run test:e2e
```

## 🔧 BMAD Methodology

This project follows the [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) for agile AI-driven development:

- **Analyst Agent** - Requirements analysis and refinement
- **Architect Agent** - Technical design and architecture decisions
- **Developer Agent** - Code implementation and testing
- **QA Agent** - Quality assurance and validation
- **Project Manager** - Project coordination and progress tracking

### BMAD Commands

- `*help` - Show available commands
- `*analyst` - Engage requirements analyst
- `*architect` - Get technical guidance
- `*developer` - Request development assistance
- `*qa` - Quality assurance review
- `*pm` - Project management support

## 🚀 Deployment

### Development Environment

```bash
docker-compose up -d
```

### Production Deployment

```bash
# Build production images
docker build -t hero-foundry:latest .

# Deploy with Kubernetes
kubectl apply -f k8s/
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/contributing.md) for details on:

- Code of Conduct
- Development Setup
- Pull Request Process
- Issue Reporting
- Community Guidelines

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation:** [Project Docs](docs/)
- **Issues:** [GitHub Issues](https://github.com/your-org/the-hero-foundry/issues)
- **Discussions:** [GitHub Discussions](https://github.com/your-org/the-hero-foundry/discussions)
- **Wiki:** [Project Wiki](https://github.com/your-org/the-hero-foundry/wiki)

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Frontend powered by [React](https://reactjs.org/)
- Database management with [SQLAlchemy](https://www.sqlalchemy.org/)
- Development methodology by [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)

---

**Made with ❤️ by The Hero Foundry Team**

*Transform your ideas into epic hero stories with The Hero Foundry!*


