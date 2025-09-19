# Development Workflow

Learn the Git workflow and development process for KNIv2.

## Branch Strategy

```
main (production releases)
├── staging (integration branch)
└── feature/feature-name (development)
```

## Git Workflow

1. **Feature Development**: Work on `feature/feature-name` branches based on `staging`
2. **Staging Integration**: Merge features to `staging` for integration testing
3. **Production Release**: Merge `staging` to `main` for production (every merge = release)

## Development Commands

### Git Workflow Commands

```bash
# Git workflow
make git-staging        # Switch to staging and pull latest
make git-feature        # Create new feature branch from staging
make git-release        # Merge staging to main and tag release
make git-hotfix         # Create hotfix branch from staging
```

### Development Commands

```bash
# Development
make dev                # Start development server (SQLite)
make dev-reset          # Reset local database and reload data
make dev-shell          # Open Django shell
```

### Testing Commands

```bash
# Testing
make test               # Run Django tests
make test-postgres      # Test with PostgreSQL (Docker)
make test-production    # Test with full production stack
```

### Building Commands

```bash
# Building
make build              # Build Docker image
make build-dev          # Build development Docker image
```

## Daily Development Workflow

### 1. Start New Feature

```bash
# Always base on staging
make git-staging
make git-feature  # Enter feature name when prompted
```

### 2. Development Work

```bash
# Start development server
make dev

# Make changes (hot reload enabled)
# Test changes locally
```

### 3. Commit Changes

```bash
# Multiple commits during development
git add .
git commit -m "Add user authentication models"
git commit -m "Add authentication views"
git commit -m "Add authentication tests"
```

### 4. Prepare for Pull Request

```bash
# Squash commits before PR
git rebase -i HEAD~3
# Squash into: "Add user authentication system"

# Test with PostgreSQL before pushing
make test-postgres

# Push feature branch and create PR to staging
git push origin feature/your-feature-name
```

## Release Process

### 1. Staging Integration

```bash
# After PR approval and merge to staging
make git-staging
```

This triggers CI/CD:
- Builds image: `ghcr.io/your-username/kni-app:staging`
- Pushes to GitHub Container Registry
- Triggers Dokploy staging deployment
- Staging environment gets updated

### 2. Production Release

```bash
# Test staging environment
# If ready for production, merge staging to main
make git-release  # Enter version when prompted
```

This triggers CI/CD:
- Builds image: `ghcr.io/your-username/kni-app:latest`
- Pushes to GitHub Container Registry
- Triggers Dokploy production deployment
- Production environment gets updated
- Tags release: v1.2.0

## Best Practices

### Development Best Practices

:material-check:{ .green } **Always test with PostgreSQL** before pushing to staging  
:material-check:{ .green } **Use feature branches** for all development  
:material-check:{ .green } **Keep commits small and focused**  
:material-check:{ .green } **Write tests for new features**  
:material-check:{ .green } **Update documentation** when adding features  

### Commit Message Guidelines

```bash
# Good commit messages
git commit -m "Add user authentication system"
git commit -m "Fix database migration issue"
git commit -m "Update documentation for new API"

# Avoid
git commit -m "fix"
git commit -m "updates"
git commit -m "stuff"
```

### Code Review Process

1. **Create Pull Request** to staging branch
2. **Request Review** from team members
3. **Address Feedback** and make changes
4. **Squash Commits** before merging
5. **Merge to Staging** after approval
6. **Test Staging Environment**
7. **Merge to Main** for production release

## Hotfix Process

### Emergency Fixes

```bash
# Create hotfix branch from staging
make git-hotfix  # Enter hotfix name when prompted

# Make emergency fix
git add .
git commit -m "Hotfix: Fix critical security issue"

# Test the fix
make test-postgres

# Push and create PR to staging
git push origin hotfix/fix-name

# After approval, merge to staging
# Then merge staging to main for immediate production release
```

## Branch Protection Rules

### Staging Branch
- Require pull request reviews
- Require status checks to pass
- Require branches to be up to date
- Restrict pushes to staging branch

### Main Branch
- Require pull request reviews
- Require status checks to pass
- Require branches to be up to date
- Restrict pushes to main branch
- Require linear history

## Next Steps

- [:material-arrow-right: Architecture](architecture.md) - Understand the system design
- [:material-arrow-right: Deployment](deployment.md) - Deploy to production