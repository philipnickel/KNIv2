# Welcome to KNIv2

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Quick Start**

    ---

    Get up and running with KNIv2 in minutes

    [:octicons-arrow-right-24: Quick Start Guide](quick-start.md)

-   :material-code-braces:{ .lg .middle } **Development**

    ---

    Learn the development workflow and architecture

    [:octicons-arrow-right-24: Development Guide](workflow.md)

-   :material-rocket-launch-outline:{ .lg .middle } **Deployment**

    ---

    Deploy to production with Dokploy

    [:octicons-arrow-right-24: Deployment Guide](deployment.md)

-   :material-cog:{ .lg .middle } **Architecture**

    ---

    Understand the system architecture

    [:octicons-arrow-right-24: Architecture Guide](architecture.md)

</div>

## What is KNIv2?

KNIv2 is a production-ready Django/Wagtail CMS with optimized development workflow and Dokploy deployment strategy.

### Key Features

:material-check:{ .green } **Django Best Practices** - Nginx + Gunicorn + PostgreSQL  
:material-check:{ .green } **Dokploy Optimized** - CI builds, Dokploy deploys  
:material-check:{ .green } **Staging-Based Workflow** - Clear release boundaries  
:material-check:{ .green } **Local Development** - SQLite for fast iteration  
:material-check:{ .green } **Production Parity** - PostgreSQL testing before deployment  
:material-check:{ .green } **Health Monitoring** - Health checks and rollbacks  
:material-check:{ .green } **Persistent Storage** - Proper volume management  

## Quick Start

```bash
# Clone repository
git clone <repository-url>
cd KNIv2

# Install dependencies
pip install -r requirements.txt
npm install

# Build static assets
npm run build

# Start development server
make dev

# Visit: http://localhost:8000
```

## Architecture Overview

### Production (Dokploy)
- **Nginx** + **Gunicorn** + **PostgreSQL**
- **GitHub Container Registry** for images
- **Docker Compose** for orchestration
- **Health checks** and **rollbacks**

### Development
- **Django** + **SQLite** for fast iteration
- **Hot reload** for code changes
- **PostgreSQL testing** before deployment

## Branch Strategy

```
main (production releases)
├── staging (integration branch)
└── feature/feature-name (development)
```

## Getting Help

- 📖 **Documentation**: Browse the guides in the navigation
- 🐛 **Issues**: Report bugs on [GitHub](https://github.com/your-username/KNIv2/issues)
- 💬 **Discussions**: Join the conversation on [GitHub Discussions](https://github.com/your-username/KNIv2/discussions)

---

<div class="grid cards" markdown>

-   :material-github:{ .lg .middle } **GitHub Repository**

    ---

    View the source code and contribute

    [:octicons-arrow-right-24: View on GitHub](https://github.com/your-username/KNIv2)

-   :material-docker:{ .lg .middle } **Docker Hub**

    ---

    Pull the latest Docker images

    [:octicons-arrow-right-24: View on Docker Hub](https://hub.docker.com/r/your-username/kni-app)

</div>
