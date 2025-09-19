# Quick Start Guide

Get up and running with KNIv2 in minutes.

## Prerequisites

- Python 3.11+
- Node.js 18+
- Git

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd KNIv2
```

### 2. Install Dependencies

```bash
# Install Python dependencies (creates virtual environment automatically)
make dev  # This will create .venv and install dependencies

# Install Node.js dependencies
cd kni_app && npm install
```

### 3. Build Static Assets

```bash
cd kni_app && npm run build
```

### 4. Start Development Server

```bash
# From the KNIv2 root directory
make dev
```

### 5. Access the Application

Open your browser and navigate to [http://localhost:8000](http://localhost:8000)

You should see the Wagtail welcome page: "Welcome to your new Wagtail site!"

## Makefile Commands

| Command | Purpose |
|---------|---------|
| `make dev` | Start development server (SQLite) |
| `make dev-reset` | Reset local database and reload data |
| `make dev-shell` | Open Django shell |
| `make git-staging` | Switch to staging and pull latest |
| `make git-feature` | Create new feature branch from staging |
| `make git-release` | Merge staging to main and tag release |
| `make git-hotfix` | Create hotfix branch from staging |
| `make test` | Run Django tests |
| `make test-postgres` | Test with PostgreSQL (Docker) |
| `make test-production` | Test with full production stack |
| `make build` | Build Docker image |
| `make build-dev` | Build development Docker image |

## Project Structure

```
KNIv2/
├── docs/                    # Documentation
├── static_src/             # Source static files
├── static_compiled/        # Compiled static files
├── media/                  # Media files
├── db.sqlite3             # Development database
├── Dockerfile             # Production container
├── docker-compose.prod.yml # Production services
├── docker-compose.test.yml # Testing services
├── Makefile               # Development commands
└── requirements.txt       # Python dependencies
```

## Default Admin

Check initial data loading output or create with:

```bash
make dev-shell
python manage.py createsuperuser
```

## Port Customization

```bash
DEV_HOST_PORT=8080 make dev
```

## Next Steps

- [:material-arrow-right: Development Workflow](workflow.md) - Learn the Git workflow
- [:material-arrow-right: Architecture](architecture.md) - Understand the system design
- [:material-arrow-right: Deployment](deployment.md) - Deploy to production

## Troubleshooting

### Common Issues

#### Database Migration Issues
```bash
make dev-reset
```

#### Static File Issues
```bash
npm run build
```

#### Dependency Issues
```bash
pip install -r requirements.txt
npm install
```

### Getting Help

- 📖 Check the [documentation](index.md)
- 🐛 Report issues on [GitHub](https://github.com/your-username/KNIv2/issues)
- 💬 Join discussions on [GitHub Discussions](https://github.com/your-username/KNIv2/discussions)