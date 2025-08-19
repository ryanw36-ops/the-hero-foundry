# Archon Setup Guide for The Hero Foundry

This guide will help you set up Archon according to the official creators' recommendations for seamless integration with Cursor IDE.

## What is Archon?

Archon is a knowledge and task management backbone for AI coding assistants. It provides:

- **Knowledge Management**: Smart web crawling, document processing, and vector search
- **AI Integration**: Model Context Protocol (MCP) for seamless tool integration
- **Project Management**: Hierarchical projects with AI-assisted task creation
- **Real-time Collaboration**: WebSocket updates and multi-user support

## Architecture Overview

Archon uses a microservices architecture with these components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend UI   │    │  Server (API)   │    │   MCP Server    │    │ Agents Service  │
│                 │    │                 │    │                 │    │                 │
│  React + Vite   │◄──►│    FastAPI +    │◄──►│    Lightweight  │◄──►│   PydanticAI    │
│  Port 3737      │    │    SocketIO     │    │    HTTP Wrapper │    │   Port 8052     │
│                 │    │    Port 8181    │    │    Port 8051    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │                        │
         └────────────────────────┼────────────────────────┼────────────────────────┘
                                  │                        │
                         ┌─────────────────┐               │
                         │    Database     │               │
                         │                 │               │
                         │    Supabase     │◄──────────────┘
                         │    PostgreSQL   │
                         │    PGVector     │
                         └─────────────────┘
```

## Prerequisites

- Docker Desktop installed and running
- Docker Compose available
- At least 4GB RAM available for containers
- Ports 3737, 8181, 8051, 8052, 5432, 6379 available

## Quick Setup

### 1. Automatic Setup (Recommended)

**For Windows (PowerShell):**
```powershell
# Navigate to your project directory
cd "The Hero Foundry"

# Run the setup script
.\scripts\setup-archon.ps1
```

**For Linux/macOS:**
```bash
# Navigate to your project directory
cd "The Hero Foundry"

# Make script executable
chmod +x scripts/setup-archon.sh

# Run the setup script
./scripts/setup-archon.sh
```

### 2. Manual Setup

If you prefer to set up manually:

1. **Create environment file:**
   ```bash
   cp archon.env.example .env
   # Edit .env with your API keys and configuration
   ```

2. **Start services:**
   ```bash
   docker-compose up -d
   ```

3. **Check service health:**
   ```bash
   docker-compose ps
   ```

## Service Ports

| Service            | Port | URL                     | Purpose                           |
| ------------------ | ---- | ----------------------- | --------------------------------- |
| **Web Interface**  | 3737 | http://localhost:3737   | Main dashboard and controls       |
| **API Service**    | 8181 | http://localhost:8181   | Web crawling, document processing |
| **MCP Server**     | 8051 | http://localhost:8051   | Model Context Protocol interface  |
| **Agents Service** | 8052 | http://localhost:8052   | AI/ML operations, reranking       |
| **Database**       | 5432 | localhost:5432          | PostgreSQL with PGVector          |
| **Cache**          | 6379 | localhost:6379          | Redis cache                       |

## Cursor Integration

### 1. Get MCP Connection Details

1. Open Archon UI: http://localhost:3737
2. Navigate to **MCP Dashboard**
3. Copy the connection configuration for your AI coding assistant

### 2. Configure Cursor

1. Open Cursor IDE
2. Go to Settings → Extensions → MCP
3. Add new MCP server with the connection details from Archon
4. Test the connection

### 3. Available MCP Tools

Archon provides 10 MCP tools:

- **Knowledge Base Management**: Upload documents, crawl websites
- **RAG Queries**: Search knowledge base with AI assistance
- **Project Management**: Create and manage projects and tasks
- **Document Processing**: Process PDFs, Word docs, markdown
- **Web Crawling**: Automatically crawl documentation sites
- **AI Agents**: Access to specialized AI agents for different tasks
- **Source Management**: Organize knowledge by source and type
- **Search & Retrieval**: Advanced semantic search capabilities
- **Session Management**: Track and manage active sessions
- **Health Monitoring**: System health and status checks

## Configuration

### Environment Variables

Key configuration options in your `.env` file:

```bash
# AI Model API Keys (Optional but recommended)
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
GOOGLE_API_KEY=your-google-api-key-here
OLLAMA_BASE_URL=http://localhost:11434

# Custom Ports (if needed)
ARCHON_UI_PORT=3737
ARCHON_SERVER_PORT=8181
ARCHON_MCP_PORT=8051
ARCHON_AGENTS_PORT=8052

# Hostname (for remote access)
HOST=localhost
```

### Custom Ports

To use different ports, modify your `.env` file:

```bash
ARCHON_SERVER_PORT=8282
ARCHON_MCP_PORT=8151
```

Then restart: `docker-compose down && docker-compose up -d`

## Usage

### 1. Initial Setup

1. Open http://localhost:3737
2. Complete the initial configuration
3. Add your first knowledge base source

### 2. Add Knowledge Sources

- **Web Crawling**: Enter URLs to automatically crawl documentation
- **Document Upload**: Upload PDFs, Word docs, markdown files
- **Manual Entry**: Add text content directly

### 3. Create Projects

1. Go to Projects section
2. Create new project with AI assistance
3. Add tasks and track progress

### 4. Use with Cursor

Once configured, you can:
- Ask questions about your codebase
- Get AI-assisted code generation
- Access project documentation
- Manage tasks and projects

## Troubleshooting

### Common Issues

1. **Port conflicts:**
   ```bash
   # Check what's using the ports
   netstat -an | findstr :3737
   netstat -an | findstr :8051
   ```

2. **Service not starting:**
   ```bash
   # Check logs
   docker-compose logs archon-server
   docker-compose logs archon-mcp
   ```

3. **Database connection issues:**
   ```bash
   # Check database status
   docker-compose logs postgres
   ```

### Reset Everything

```bash
# Stop and remove all containers
docker-compose down -v

# Remove all images
docker rmi $(docker images -q)

# Start fresh
docker-compose up -d
```

## Development

For development with hot reload:

```bash
# Backend services (with auto-reload)
docker-compose up archon-server archon-mcp archon-agents --build

# Frontend (with hot reload)
cd archon-ui-main && npm run dev
```

## Support

- **Official Documentation**: [Archon GitHub](https://github.com/coleam00/Archon)
- **Issues**: [GitHub Issues](https://github.com/coleam00/Archon/issues)
- **Discussions**: [GitHub Discussions](https://github.com/coleam00/Archon/discussions)

## Next Steps

After setup:

1. **Explore the UI**: Familiarize yourself with the dashboard
2. **Add Knowledge**: Upload your project documentation
3. **Create Projects**: Set up your Hero Foundry project
4. **Configure Cursor**: Connect your IDE for seamless development
5. **Start Building**: Use Archon's AI capabilities to enhance your development workflow

---

**Note**: This setup follows the official Archon recommendations and provides the full microservices architecture as intended by the creators. Your custom MCP server files can be removed once this setup is working.
