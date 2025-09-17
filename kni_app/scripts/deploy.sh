#!/bin/bash
set -euo pipefail

# Deployment script for KNI Django/Wagtail application
# This script ensures proper build validation and deployment health checks

echo "🚀 Starting KNI deployment process..."

# Configuration
DOCKER_TAG=${DOCKER_TAG:-"kni:latest"}
SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-"KNI.settings.production"}

# Function to log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to run health checks
run_health_check() {
    log "Running health checks..."
    if docker run --rm "$DOCKER_TAG" python scripts/deployment_health_check.py; then
        log "✅ Health check passed"
        return 0
    else
        log "❌ Health check failed"
        return 1
    fi
}

# Build Docker image
log "Building Docker image: $DOCKER_TAG"
docker build -t "$DOCKER_TAG" .

# Validate the build
log "Validating Docker build..."
if ! run_health_check; then
    log "❌ Build validation failed. Trying with fallback settings..."

    # Try building with fallback settings
    docker build -t "${DOCKER_TAG}-fallback" \
        --build-arg DJANGO_SETTINGS_MODULE=KNI.settings.production_fallback .

    if docker run --rm "${DOCKER_TAG}-fallback" python scripts/deployment_health_check.py; then
        log "✅ Fallback build successful"
        DOCKER_TAG="${DOCKER_TAG}-fallback"
    else
        log "❌ Both main and fallback builds failed. Aborting deployment."
        exit 1
    fi
fi

# Test the container
log "Testing container startup..."
CONTAINER_ID=$(docker run -d \
    -p 8000:8000 \
    -e SECRET_KEY=test-deployment-key \
    -e DJANGO_SETTINGS_MODULE="$SETTINGS_MODULE" \
    -e ALLOWED_HOSTS=localhost \
    "$DOCKER_TAG")

# Wait for container to be ready
log "Waiting for container to start..."
sleep 10

# Check if container is still running
if docker ps | grep -q "$CONTAINER_ID"; then
    log "✅ Container started successfully"

    # Test health endpoint (if available)
    if curl -f http://localhost:8000/ >/dev/null 2>&1; then
        log "✅ Application responding to HTTP requests"
    else
        log "⚠️  Application not responding to HTTP requests (may need DB setup)"
    fi
else
    log "❌ Container failed to start"
    docker logs "$CONTAINER_ID"
    docker rm "$CONTAINER_ID" >/dev/null 2>&1 || true
    exit 1
fi

# Cleanup test container
docker stop "$CONTAINER_ID" >/dev/null
docker rm "$CONTAINER_ID" >/dev/null

log "🎉 Deployment validation completed successfully!"
log "Docker image ready: $DOCKER_TAG"

# Deployment instructions
cat << EOF

📋 Deployment Instructions:

1. For Dokploy deployment, use the validated image:
   $DOCKER_TAG

2. Environment variables to set:
   - SECRET_KEY=<your-production-secret>
   - DJANGO_SETTINGS_MODULE=$SETTINGS_MODULE
   - ALLOWED_HOSTS=<your-domain>
   - DATABASE_URL=<your-database-url>

3. If deployment fails, try the fallback settings:
   - DJANGO_SETTINGS_MODULE=KNI.settings.production_fallback

4. Monitor logs for static file issues:
   docker logs <container-id> | grep -i "static\|manifest\|favicon"

EOF