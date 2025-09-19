# Project Structure

This document outlines the clean, organized structure of the KNIv2 repository.

## 📁 Repository Structure

```
KNIv2/
├── 📁 docs/                          # Documentation
│   ├── index.md                      # Main documentation homepage
│   ├── quick-start.md                # Quick start guide
│   ├── workflow.md                   # Development workflow
│   ├── architecture.md               # System architecture
│   ├── deployment.md                 # Deployment guide
│   ├── PRODUCTION_DEPLOYMENT.md      # Production setup
│   ├── README.md                     # Documentation setup guide
│   └── build.sh                      # Documentation build script
│
├── 📁 scripts/                       # Deployment scripts
│   ├── deploy_production.sh          # Production deployment script
│   ├── deploy.sh                     # General deployment script
│   └── deployment_health_check.py    # Health check script
│
├── 📁 kni_app/                       # Django application
│   ├── 📁 KNI/                       # Django project settings
│   │   ├── settings/                 # Environment-specific settings
│   │   ├── forms/                    # Form definitions
│   │   ├── home/                     # Home page app
│   │   ├── images/                   # Image handling app
│   │   ├── navigation/               # Navigation app
│   │   ├── news/                     # News app
│   │   ├── search/                   # Search functionality
│   │   ├── standardpages/            # Standard page types
│   │   ├── users/                    # User management
│   │   ├── utils/                    # Utility functions
│   │   ├── urls.py                   # URL configuration
│   │   └── wsgi.py                   # WSGI configuration
│   │
│   ├── 📁 templates/                 # Django templates
│   │   ├── base.html                 # Base template
│   │   ├── components/               # Reusable components
│   │   ├── icons/                    # Icon templates
│   │   ├── navigation/               # Navigation templates
│   │   └── pages/                    # Page templates
│   │
│   ├── 📁 static_src/                # Source static files
│   │   ├── fonts/                    # Font files
│   │   ├── images/                   # Source images
│   │   ├── javascript/               # JavaScript source
│   │   └── sass/                     # Sass stylesheets
│   │
│   ├── 📁 static_compiled/           # Compiled static files
│   ├── 📁 static/                    # Django static files
│   ├── 📁 media/                     # User-uploaded media
│   ├── 📁 fixtures/                  # Database fixtures
│   │
│   ├── Dockerfile                    # Docker container definition
│   ├── Makefile                      # Development commands
│   ├── manage.py                     # Django management script
│   ├── requirements.txt              # Python dependencies
│   ├── package.json                  # Node.js dependencies
│   ├── webpack.config.js             # Webpack configuration
│   ├── tailwind.config.js            # Tailwind CSS configuration
│   ├── tsconfig.json                 # TypeScript configuration
│   ├── gunicorn.conf.py              # Gunicorn configuration
│   └── fly.toml                      # Fly.io configuration
│
├── 📁 .github/                       # GitHub configuration
│   └── workflows/                    # GitHub Actions workflows
│       ├── ci.yml                    # Continuous Integration
│       └── docs.yml                  # Documentation deployment
│
├── docker-compose.prod.yml           # Production Docker Compose
├── docker-compose.test.yml           # Testing Docker Compose
├── nginx.conf                        # Nginx configuration
├── mkdocs.yml                        # MkDocs configuration
├── requirements-docs.txt             # Documentation dependencies
├── .readthedocs.yml                  # Read the Docs configuration
├── .gitignore                        # Git ignore rules
├── README.md                         # Main project README
└── PROJECT_STRUCTURE.md              # This file
```

## 🎯 Organization Principles

### 1. **Clear Separation of Concerns**
- **`docs/`**: All documentation in one place
- **`scripts/`**: Deployment and utility scripts
- **`kni_app/`**: Django application code
- **Root level**: Configuration and deployment files

### 2. **Documentation First**
- All documentation in `docs/` directory
- MkDocs with Material theme for beautiful presentation
- Read the Docs integration for professional hosting

### 3. **Deployment Ready**
- Docker Compose files at root level
- Nginx configuration for production
- Deployment scripts in dedicated directory

### 4. **Development Friendly**
- Makefile with common commands
- Clear project structure
- Comprehensive .gitignore

## 📋 Key Files

### Configuration Files
- **`mkdocs.yml`**: Documentation configuration
- **`docker-compose.prod.yml`**: Production deployment
- **`nginx.conf`**: Web server configuration
- **`.readthedocs.yml`**: Read the Docs setup

### Development Files
- **`kni_app/Makefile`**: Development commands
- **`kni_app/requirements.txt`**: Python dependencies
- **`kni_app/package.json`**: Node.js dependencies
- **`requirements-docs.txt`**: Documentation dependencies

### Deployment Files
- **`scripts/deploy_production.sh`**: Production deployment
- **`scripts/deployment_health_check.py`**: Health monitoring
- **`docker-compose.prod.yml`**: Production services

## 🚀 Benefits of This Structure

### ✅ **Clean Organization**
- No scattered files
- Clear directory purposes
- Easy to navigate

### ✅ **Professional Documentation**
- MkDocs with Material theme
- Read the Docs integration
- Search and navigation

### ✅ **Production Ready**
- Docker Compose deployment
- Nginx configuration
- Health checks and monitoring

### ✅ **Developer Friendly**
- Clear Makefile commands
- Comprehensive documentation
- Easy local development

### ✅ **CI/CD Ready**
- GitHub Actions workflows
- Automated testing
- Automated documentation deployment

## 🔧 Development Workflow

### Local Development
```bash
cd kni_app
make dev                    # Start development server
make test-postgres         # Test with PostgreSQL
make docs-serve            # Serve documentation locally
```

### Documentation
```bash
make docs-build            # Build documentation
make docs-serve            # Serve documentation locally
make docs-clean            # Clean build files
```

### Deployment
```bash
make git-staging           # Switch to staging
make git-feature           # Create feature branch
make git-release           # Release to production
```

## 📖 Documentation

- **[📖 Read the Docs](https://kniv2.readthedocs.io/)** - Full documentation
- **[Quick Start](docs/quick-start.md)** - Get started quickly
- **[Workflow](docs/workflow.md)** - Development process
- **[Architecture](docs/architecture.md)** - System design
- **[Deployment](docs/deployment.md)** - Production deployment

This structure provides a clean, professional, and maintainable codebase that follows Django and deployment best practices.
