# KNIv2

Production-ready Django/Wagtail CMS with optimized development workflow and Dokploy deployment strategy.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start development server
make dev

# Visit: http://localhost:8000
```

## Development Commands

```bash
make dev                # Start development server
make dev-reset          # Reset database and reload data
make test               # Run tests
make docs-serve         # Serve documentation locally
```

## Documentation

- **[Quick Start](docs/quick-start.md)** - Get up and running quickly
- **[Development Workflow](docs/workflow.md)** - Git workflow and development process
- **[Architecture](docs/architecture.md)** - System architecture and technology stack
- **[Deployment](docs/deployment.md)** - Production deployment with Dokploy
- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - Repository organization

## Architecture

- **Development**: Django + SQLite for fast iteration
- **Production**: Nginx + Gunicorn + PostgreSQL
- **Deployment**: Dokploy with Docker Compose
- **CI/CD**: GitHub Actions with staging-based workflow

## Key Features

- ✅ Django/Wagtail CMS
- ✅ Staging-based Git workflow
- ✅ Docker containerization
- ✅ Health checks and monitoring
- ✅ Comprehensive documentation