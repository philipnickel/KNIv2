# KNIv2 Development Makefile
# This file provides convenient commands for development, testing, and deployment

# Variables
DOCKER := docker
DOCKER_COMPOSE := docker-compose
PROJECT_ROOT := $(shell pwd)
MANAGE_RUN_FLAGS := -e DJANGO_SETTINGS_MODULE=KNI.settings.dev

# Development commands
.PHONY: dev dev-reset dev-shell test test-postgres test-production build build-dev git-staging git-feature git-release git-hotfix docs-build docs-serve docs-clean

# Development server
dev:
	@echo "🚀 Starting development server..."
	@if [ ! -d ".venv" ]; then \
		echo "📦 Creating virtual environment..."; \
		python3 -m venv .venv; \
		echo "📦 Installing dependencies..."; \
		.venv/bin/pip install -r requirements.txt; \
	fi
	cd kni_app && ../.venv/bin/python manage.py runserver 0.0.0.0:8000

# Reset development database
dev-reset:
	@echo "🔄 Resetting development database..."
	cd kni_app && rm -f db.sqlite3
	cd kni_app && ../.venv/bin/python manage.py migrate
	cd kni_app && ../.venv/bin/python manage.py loaddata fixtures/demo.json
	@echo "✅ Database reset complete!"

# Django shell
dev-shell:
	@echo "🐍 Opening Django shell..."
	cd kni_app && ../.venv/bin/python manage.py shell

# Run tests
test:
	@echo "🧪 Running Django tests..."
	cd kni_app && ../.venv/bin/python manage.py test

# Test with PostgreSQL (Docker)
test-postgres:
	@echo "🐘 Testing with PostgreSQL..."
	$(DOCKER_COMPOSE) -f docker-compose.test.yml up --build --abort-on-container-exit
	$(DOCKER_COMPOSE) -f docker-compose.test.yml down

# Test with full production stack
test-production:
	@echo "🏭 Testing with production stack..."
	$(DOCKER_COMPOSE) -f docker-compose.prod.yml up --build --abort-on-container-exit
	$(DOCKER_COMPOSE) -f docker-compose.prod.yml down

# Build Docker image
build:
	@echo "🔨 Building Docker image..."
	cd kni_app && $(DOCKER) build -t kni-app:latest .

# Build development Docker image
build-dev:
	@echo "🔨 Building development Docker image..."
	cd kni_app && $(DOCKER) build -f Dockerfile.dev -t kni-app:dev .

# Git workflow commands
git-staging:
	@echo "📋 Switching to staging branch..."
	git checkout staging
	git pull origin staging

git-feature:
	@echo "🌿 Creating new feature branch..."
	@read -p "Enter feature name: " name; \
	git checkout -b feature_$$name staging

git-release:
	@echo "🚀 Creating release..."
	git checkout main
	git merge staging
	git push origin main
	@read -p "Enter release version: " version; \
	git tag -a v$$version -m "Release v$$version"
	git push origin v$$version

git-hotfix:
	@echo "🔧 Creating hotfix branch..."
	@read -p "Enter hotfix name: " name; \
	git checkout -b hotfix_$$name staging

# Documentation commands
docs-build:
	cd docs && mkdocs build

docs-serve:
	cd docs && mkdocs serve

docs-clean:
	cd docs && rm -rf site/

# Production database migration
migrate-prod: build
	$(DOCKER) run --rm $(MANAGE_RUN_FLAGS) \
		-v $(PROJECT_ROOT)/kni_app:/app \
		-e DJANGO_SETTINGS_MODULE=KNI.settings.production \
		kni-app:latest python manage.py migrate

# Collect static files for production
collectstatic-prod: build
	$(DOCKER) run --rm $(MANAGE_RUN_FLAGS) \
		-v $(PROJECT_ROOT)/kni_app:/app \
		-e DJANGO_SETTINGS_MODULE=KNI.settings.production \
		kni-app:latest python manage.py collectstatic --noinput

# Help
help:
	@echo "Available commands:"
	@echo "  dev              - Start development server"
	@echo "  dev-reset        - Reset development database"
	@echo "  dev-shell        - Open Django shell"
	@echo "  test             - Run Django tests"
	@echo "  test-postgres    - Test with PostgreSQL (Docker)"
	@echo "  test-production  - Test with full production stack"
	@echo "  build            - Build Docker image"
	@echo "  build-dev        - Build development Docker image"
	@echo "  git-staging      - Switch to staging branch"
	@echo "  git-feature      - Create new feature branch"
	@echo "  git-release      - Create release"
	@echo "  git-hotfix       - Create hotfix branch"
	@echo "  docs-build       - Build documentation"
	@echo "  docs-serve       - Serve documentation locally"
	@echo "  docs-clean       - Clean documentation build files"
	@echo "  help             - Show this help message"
