# Source Tree - The Hero Foundry

## Overview
This document outlines the complete source code structure for The Hero Foundry project, including all directories, files, and their purposes.

## Project Root Structure
```
The Hero Foundry/
├── .bmad-core/                 # BMAD methodology core files
├── .cursor/                    # Cursor IDE configuration and rules
├── .ai/                        # AI development artifacts and logs
├── docs/                       # Project documentation
├── src/                        # Source code
├── tests/                      # Test files
├── scripts/                    # Utility and deployment scripts
├── docker/                     # Docker configuration files
├── .github/                    # GitHub configuration and workflows
├── .vscode/                    # VS Code configuration (optional)
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Python project configuration
├── package.json               # Node.js dependencies (frontend)
├── README.md                  # Project overview and setup
├── .gitignore                 # Git ignore patterns
├── .env.example               # Environment variables template
└── docker-compose.yml         # Local development environment
```

## Source Code Structure

### Backend Source (`src/`)
```
src/
├── hero_foundry/              # Main Python package
│   ├── __init__.py            # Package initialization
│   ├── main.py                # FastAPI application entry point
│   ├── config.py              # Configuration management
│   ├── core/                  # Core application components
│   │   ├── __init__.py
│   │   ├── security.py        # Security and authentication
│   │   ├── database.py        # Database connection and session
│   │   ├── cache.py           # Redis cache management
│   │   └── exceptions.py      # Custom exception classes
│   ├── models/                # Database models and schemas
│   │   ├── __init__.py
│   │   ├── base.py            # Base model class
│   │   ├── user.py            # User model and schemas
│   │   ├── hero.py            # Hero model and schemas
│   │   ├── story.py           # Story model and schemas
│   │   ├── quest.py           # Quest model and schemas
│   │   ├── skill.py           # Skill model and schemas
│   │   ├── attribute.py       # Attribute model and schemas
│   │   ├── team.py            # Team and collaboration models
│   │   └── content.py         # Content and media models
│   ├── services/              # Business logic services
│   │   ├── __init__.py
│   │   ├── user_service.py    # User management service
│   │   ├── hero_service.py    # Hero management service
│   │   ├── story_service.py   # Story management service
│   │   ├── quest_service.py   # Quest management service
│   │   ├── content_service.py # Content management service
│   │   ├── export_service.py  # Content export service
│   │   ├── auth_service.py    # Authentication service
│   │   └── team_service.py    # Team collaboration service
│   ├── api/                   # API endpoints and routes
│   │   ├── __init__.py
│   │   ├── deps.py            # Dependency injection
│   │   ├── middleware.py      # Custom middleware
│   │   ├── routes/            # API route modules
│   │   │   ├── __init__.py
│   │   │   ├── auth.py        # Authentication routes
│   │   │   ├── users.py       # User management routes
│   │   │   ├── heroes.py      # Hero management routes
│   │   │   ├── stories.py     # Story management routes
│   │   │   ├── quests.py      # Quest management routes
│   │   │   ├── content.py     # Content management routes
│   │   │   ├── export.py      # Export functionality routes
│   │   │   └── teams.py       # Team collaboration routes
│   │   └── graphql/           # GraphQL schema and resolvers
│   │       ├── __init__.py
│   │       ├── schema.py      # GraphQL schema definition
│   │       ├── resolvers/     # GraphQL resolvers
│   │       │   ├── __init__.py
│   │       │   ├── user.py    # User resolvers
│   │       │   ├── hero.py    # Hero resolvers
│   │       │   ├── story.py   # Story resolvers
│   │       │   └── quest.py   # Quest resolvers
│   │       └── types.py       # GraphQL type definitions
│   ├── utils/                 # Utility functions and helpers
│   │   ├── __init__.py
│   │   ├── helpers.py         # General helper functions
│   │   ├── validators.py      # Data validation utilities
│   │   ├── formatters.py      # Data formatting utilities
│   │   ├── security.py        # Security utility functions
│   │   └── constants.py       # Application constants
│   ├── tasks/                 # Background task definitions
│   │   ├── __init__.py
│   │   ├── celery_app.py      # Celery application configuration
│   │   ├── hero_tasks.py      # Hero-related background tasks
│   │   ├── story_tasks.py     # Story-related background tasks
│   │   ├── export_tasks.py    # Export-related background tasks
│   │   └── notification_tasks.py # Notification tasks
│   └── migrations/            # Database migration scripts
│       ├── __init__.py
│       ├── env.py             # Migration environment
│       ├── script.py.mako     # Migration template
│       └── versions/          # Migration version files
│           ├── __init__.py
│           ├── 001_initial.py # Initial database schema
│           ├── 002_users.py   # User table creation
│           ├── 003_heroes.py  # Hero table creation
│           └── 004_stories.py # Story table creation
```

### Frontend Source (`frontend/`)
```
frontend/
├── public/                    # Static assets
│   ├── index.html            # Main HTML file
│   ├── favicon.ico           # Favicon
│   ├── manifest.json         # PWA manifest
│   └── assets/               # Static images and files
│       ├── images/           # Image assets
│       ├── icons/            # Icon assets
│       └── fonts/            # Custom fonts
├── src/                      # React source code
│   ├── main.tsx             # Application entry point
│   ├── App.tsx              # Main application component
│   ├── index.css            # Global styles
│   ├── components/           # Reusable UI components
│   │   ├── common/          # Common UI components
│   │   │   ├── Button.tsx   # Button component
│   │   │   ├── Input.tsx    # Input field component
│   │   │   ├── Modal.tsx    # Modal dialog component
│   │   │   ├── Card.tsx     # Card component
│   │   │   └── Loading.tsx  # Loading spinner component
│   │   ├── layout/          # Layout components
│   │   │   ├── Header.tsx   # Application header
│   │   │   ├── Sidebar.tsx  # Navigation sidebar
│   │   │   ├── Footer.tsx   # Application footer
│   │   │   └── Layout.tsx   # Main layout wrapper
│   │   ├── hero/            # Hero-related components
│   │   │   ├── HeroCard.tsx # Hero display card
│   │   │   ├── HeroForm.tsx # Hero creation/editing form
│   │   │   ├── HeroList.tsx # Hero list component
│   │   │   ├── HeroView.tsx # Hero detail view
│   │   │   └── HeroStats.tsx # Hero statistics display
│   │   ├── story/           # Story-related components
│   │   │   ├── StoryCard.tsx # Story display card
│   │   │   ├── StoryForm.tsx # Story creation/editing form
│   │   │   ├── StoryList.tsx # Story list component
│   │   │   ├── StoryView.tsx # Story detail view
│   │   │   └── StoryBuilder.tsx # Story building interface
│   │   ├── quest/           # Quest-related components
│   │   │   ├── QuestCard.tsx # Quest display card
│   │   │   ├── QuestForm.tsx # Quest creation/editing form
│   │   │   ├── QuestList.tsx # Quest list component
│   │   │   └── QuestView.tsx # Quest detail view
│   │   ├── user/            # User-related components
│   │   │   ├── LoginForm.tsx # User login form
│   │   │   ├── RegisterForm.tsx # User registration form
│   │   │   ├── UserProfile.tsx # User profile display
│   │   │   └── UserSettings.tsx # User settings form
│   │   └── team/            # Team collaboration components
│   │       ├── TeamCard.tsx # Team display card
│   │       ├── TeamForm.tsx # Team creation/editing form
│   │       ├── TeamList.tsx # Team list component
│   │       └── TeamView.tsx # Team detail view
│   ├── pages/               # Page components
│   │   ├── Home.tsx         # Home page
│   │   ├── Heroes.tsx       # Heroes page
│   │   ├── Stories.tsx      # Stories page
│   │   ├── Quests.tsx       # Quests page
│   │   ├── Profile.tsx      # User profile page
│   │   ├── Teams.tsx        # Teams page
│   │   ├── Export.tsx       # Export page
│   │   └── Admin.tsx        # Admin dashboard page
│   ├── hooks/               # Custom React hooks
│   │   ├── useAuth.ts       # Authentication hook
│   │   ├── useHeroes.ts     # Hero data hook
│   │   ├── useStories.ts    # Story data hook
│   │   ├── useQuests.ts     # Quest data hook
│   │   ├── useUsers.ts      # User data hook
│   │   ├── useTeams.ts      # Team data hook
│   │   └── useExport.ts     # Export functionality hook
│   ├── services/            # API service functions
│   │   ├── api.ts           # Base API configuration
│   │   ├── auth.ts          # Authentication API calls
│   │   ├── heroes.ts        # Hero API calls
│   │   ├── stories.ts       # Story API calls
│   │   ├── quests.ts        # Quest API calls
│   │   ├── users.ts         # User API calls
│   │   ├── teams.ts         # Team API calls
│   │   └── export.ts        # Export API calls
│   ├── store/               # State management
│   │   ├── index.ts         # Store configuration
│   │   ├── authSlice.ts     # Authentication state
│   │   ├── heroSlice.ts     # Hero state
│   │   ├── storySlice.ts    # Story state
│   │   ├── questSlice.ts    # Quest state
│   │   ├── userSlice.ts     # User state
│   │   └── teamSlice.ts     # Team state
│   ├── types/               # TypeScript type definitions
│   │   ├── index.ts         # Type exports
│   │   ├── hero.ts          # Hero-related types
│   │   ├── story.ts         # Story-related types
│   │   ├── quest.ts         # Quest-related types
│   │   ├── user.ts          # User-related types
│   │   ├── team.ts          # Team-related types
│   │   └── api.ts           # API response types
│   ├── utils/               # Utility functions
│   │   ├── constants.ts     # Application constants
│   │   ├── helpers.ts       # Helper functions
│   │   ├── validators.ts    # Validation functions
│   │   ├── formatters.ts    # Data formatting functions
│   │   └── storage.ts       # Local storage utilities
│   └── styles/              # Styling files
│       ├── globals.css      # Global CSS styles
│       ├── components.css   # Component-specific styles
│       └── variables.css    # CSS custom properties
```

## Test Structure

### Backend Tests (`tests/`)
```
tests/
├── __init__.py               # Test package initialization
├── conftest.py              # Pytest configuration and fixtures
├── unit/                    # Unit tests
│   ├── __init__.py
│   ├── test_models/         # Model tests
│   │   ├── __init__.py
│   │   ├── test_user.py     # User model tests
│   │   ├── test_hero.py     # Hero model tests
│   │   ├── test_story.py    # Story model tests
│   │   └── test_quest.py    # Quest model tests
│   ├── test_services/       # Service tests
│   │   ├── __init__.py
│   │   ├── test_user_service.py # User service tests
│   │   ├── test_hero_service.py # Hero service tests
│   │   ├── test_story_service.py # Story service tests
│   │   └── test_quest_service.py # Quest service tests
│   ├── test_utils/          # Utility tests
│   │   ├── __init__.py
│   │   ├── test_helpers.py  # Helper function tests
│   │   ├── test_validators.py # Validator tests
│   │   └── test_formatters.py # Formatter tests
│   └── test_tasks/          # Background task tests
│       ├── __init__.py
│       ├── test_hero_tasks.py # Hero task tests
│       └── test_story_tasks.py # Story task tests
├── integration/              # Integration tests
│   ├── __init__.py
│   ├── test_api/            # API integration tests
│   │   ├── __init__.py
│   │   ├── test_auth.py     # Authentication API tests
│   │   ├── test_heroes.py   # Hero API tests
│   │   ├── test_stories.py  # Story API tests
│   │   └── test_quests.py   # Quest API tests
│   ├── test_database/       # Database integration tests
│   │   ├── __init__.py
│   │   ├── test_models.py   # Model integration tests
│   │   └── test_migrations.py # Migration tests
│   └── test_services/       # Service integration tests
│       ├── __init__.py
│       ├── test_auth_integration.py # Auth service integration
│       └── test_hero_integration.py # Hero service integration
└── e2e/                     # End-to-end tests
    ├── __init__.py
    ├── test_user_workflow.py # Complete user workflow tests
    ├── test_hero_creation.py # Hero creation workflow tests
    └── test_story_building.py # Story building workflow tests
```

### Frontend Tests (`frontend/tests/`)
```
frontend/tests/
├── __init__.py               # Test package initialization
├── components/               # Component tests
│   ├── test_common/         # Common component tests
│   │   ├── Button.test.tsx  # Button component tests
│   │   ├── Input.test.tsx   # Input component tests
│   │   └── Modal.test.tsx   # Modal component tests
│   ├── test_hero/           # Hero component tests
│   │   ├── HeroCard.test.tsx # Hero card tests
│   │   ├── HeroForm.test.tsx # Hero form tests
│   │   └── HeroList.test.tsx # Hero list tests
│   └── test_story/          # Story component tests
│       ├── StoryCard.test.tsx # Story card tests
│       ├── StoryForm.test.tsx # Story form tests
│       └── StoryList.test.tsx # Story list tests
├── pages/                    # Page tests
│   ├── Home.test.tsx        # Home page tests
│   ├── Heroes.test.tsx      # Heroes page tests
│   └── Stories.test.tsx     # Stories page tests
├── hooks/                    # Hook tests
│   ├── useAuth.test.ts      # Auth hook tests
│   ├── useHeroes.test.ts    # Hero hook tests
│   └── useStories.test.ts   # Story hook tests
├── services/                 # Service tests
│   ├── api.test.ts          # API service tests
│   ├── auth.test.ts         # Auth service tests
│   └── heroes.test.ts       # Hero service tests
└── utils/                    # Utility tests
    ├── helpers.test.ts      # Helper function tests
    ├── validators.test.ts   # Validator tests
    └── formatters.test.ts   # Formatter tests
```

## Configuration Files

### Python Configuration
```
pyproject.toml               # Python project configuration
requirements.txt             # Python dependencies
requirements-dev.txt         # Development dependencies
.python-version             # Python version specification
```

### Frontend Configuration
```
package.json                # Node.js dependencies and scripts
vite.config.ts             # Vite build configuration
tsconfig.json              # TypeScript configuration
.eslintrc.js               # ESLint configuration
.prettierrc                # Prettier configuration
tailwind.config.js         # Tailwind CSS configuration
```

### Development Tools
```
.pre-commit-config.yaml    # Pre-commit hooks configuration
.editorconfig              # Editor configuration
.gitignore                 # Git ignore patterns
.env.example               # Environment variables template
docker-compose.yml         # Local development environment
Dockerfile                 # Application container definition
.dockerignore              # Docker ignore patterns
```

## Documentation Structure

### Project Documentation (`docs/`)
```
docs/
├── README.md               # Project overview
├── SETUP.md               # Setup and installation guide
├── API.md                 # API documentation
├── DEPLOYMENT.md          # Deployment guide
├── CONTRIBUTING.md        # Contribution guidelines
├── CHANGELOG.md           # Version change log
├── prd.md                 # Product Requirements Document
├── architecture.md        # System architecture
├── architecture/          # Architecture sub-documents
│   ├── coding-standards.md # Coding standards
│   ├── tech-stack.md      # Technology stack
│   └── source-tree.md     # Source code structure
├── qa/                    # Quality assurance documents
│   ├── test-plan.md       # Testing strategy
│   ├── test-cases.md      # Test case specifications
│   └── bug-reports.md     # Bug tracking and reports
└── stories/               # User stories and requirements
    ├── hero-stories.md    # Hero-related user stories
    ├── story-stories.md   # Story-related user stories
    └── quest-stories.md   # Quest-related user stories
```

## Scripts and Utilities

### Development Scripts (`scripts/`)
```
scripts/
├── setup.sh               # Project setup script
├── install.sh             # Dependency installation
├── test.sh                # Test execution script
├── lint.sh                # Code linting script
├── format.sh              # Code formatting script
├── build.sh               # Build script
├── deploy.sh              # Deployment script
└── utils/                 # Utility scripts
    ├── db-setup.py        # Database setup utility
    ├── seed-data.py       # Seed data generation
    └── backup.py          # Database backup utility
```

## Docker Configuration

### Docker Files (`docker/`)
```
docker/
├── Dockerfile             # Application container definition
├── Dockerfile.dev         # Development container definition
├── docker-compose.yml     # Local development environment
├── docker-compose.prod.yml # Production environment
├── nginx/                 # Nginx configuration
│   ├── nginx.conf         # Nginx main configuration
│   └── default.conf       # Default site configuration
└── postgres/              # PostgreSQL configuration
    └── init.sql           # Database initialization script
```

## GitHub Configuration

### GitHub Workflows (`.github/`)
```
.github/
├── workflows/             # GitHub Actions workflows
│   ├── ci.yml            # Continuous integration
│   ├── cd.yml            # Continuous deployment
│   ├── test.yml          # Testing workflow
│   └── release.yml       # Release workflow
├── ISSUE_TEMPLATE/        # Issue templates
│   ├── bug-report.md     # Bug report template
│   ├── feature-request.md # Feature request template
│   └── question.md       # Question template
└── PULL_REQUEST_TEMPLATE.md # Pull request template
```

---

*This source tree provides a comprehensive overview of The Hero Foundry project structure. All directories and files are organized following best practices for maintainability and scalability.*




