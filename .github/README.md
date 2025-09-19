# GitHub Workflows

This directory contains GitHub Actions workflows for the KNI project's CI/CD pipeline.

## Workflows Overview

### 🔧 [ci.yml](workflows/ci.yml) - Complete CI/CD Pipeline
The main CI/CD pipeline that runs on every push and pull request. It includes:
- **🧪 Testing**: Runs the complete test suite with coverage across Python 3.11 and 3.12
- **🔍 Code Quality**: Code quality checks with Black, isort, flake8, and mypy
- **🔒 Security**: Vulnerability scanning with Safety, Bandit, and Semgrep
- **🎭 End-to-End**: Browser-based testing with Playwright
- **🏗️ Building**: Creates deployment artifacts
- **🚀 Deployment**: Deploys to staging and production environments

### 📚 [docs.yml](workflows/docs.yml) - Documentation
Documentation building and linting:
- **Build**: Sphinx documentation generation
- **Lint**: RST file validation and link checking
- **Deploy**: Automatic deployment to GitHub Pages

### 📦 [dependencies.yml](workflows/dependencies.yml) - Dependency Management
Automated dependency updates:
- **Weekly Updates**: Checks for outdated packages
- **Automated PRs**: Creates pull requests for updates
- **Version Monitoring**: Tracks package versions

## Configuration Files

### [dependabot.yml](dependabot.yml) - Dependabot Configuration
Configures automated dependency updates for:
- Python packages (pip)
- GitHub Actions
- Weekly schedule with proper labeling

## Usage

### Running Workflows

1. **Automatic**: Workflows run automatically on:
   - Push to main, staging, or develop branches
   - Pull requests to main, staging, or develop branches
   - Scheduled runs (dependency updates)

2. **Manual**: Use the "Actions" tab in GitHub to manually trigger workflows

### Branch Strategy

- **main**: Production branch - triggers deployment
- **staging**: Staging branch - triggers staging deployment
- **develop**: Development branch - runs tests and checks

### Environment Variables

Set these secrets in your GitHub repository settings:

```bash
# Database
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=your_db_host
POSTGRES_PORT=5432

# Django
SECRET_KEY=your_secret_key
DEBUG=False

# Deployment
DEPLOY_HOST=your_deploy_host
DEPLOY_USER=your_deploy_user
DEPLOY_KEY=your_deploy_ssh_key
```

### Local Development

To run the same checks locally:

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-docs.txt

# Run tests
make test

# Run linting
black --check .
isort --check-only .
flake8 .

# Run security checks
safety check
bandit -r kni_app/

# Build documentation
cd docs
./build.sh

# Run e2e tests
playwright install
python manage.py runserver &
python -c "import asyncio; from playwright.async_api import async_playwright; ..."
```

## Workflow Status Badges

Add these badges to your README.md:

```markdown
![CI/CD](https://github.com/yourusername/KNIv2/workflows/CI%2FCD%20Pipeline/badge.svg)
![Documentation](https://github.com/yourusername/KNIv2/workflows/Documentation/badge.svg)
![Dependencies](https://github.com/yourusername/KNIv2/workflows/Dependencies/badge.svg)
```

## Workflow Jobs

### CI/CD Pipeline Jobs

1. **🧪 Test Suite**
   - Python 3.11 and 3.12 matrix
   - Django test execution
   - Coverage reporting
   - Codecov integration

2. **🔍 Code Quality**
   - Black code formatting
   - isort import sorting
   - flake8 linting
   - mypy type checking

3. **🔒 Security Checks**
   - Safety dependency scanning
   - Bandit security analysis
   - Semgrep static analysis
   - PR comments with findings

4. **🎭 End-to-End Tests**
   - Playwright browser testing
   - Django server setup
   - Screenshot capture
   - Visual verification

5. **🏗️ Build**
   - Static file collection
   - Artifact creation
   - Deployment preparation

6. **🚀 Deployment**
   - Staging deployment
   - Production deployment
   - Environment-specific configs

### Documentation Jobs

1. **📚 Build Documentation**
   - Sphinx HTML generation
   - Link checking
   - GitHub Pages deployment

2. **🔍 Lint Documentation**
   - RST file validation
   - Link checking
   - Structure validation

### Dependencies Jobs

1. **📦 Update Dependencies**
   - Package version checking
   - Automated PR creation
   - Update tracking

## Troubleshooting

### Common Issues

1. **Database Connection**: Ensure PostgreSQL service is running and accessible
2. **Dependencies**: Check that all required packages are in requirements.txt
3. **Permissions**: Verify GitHub Actions has necessary permissions
4. **Secrets**: Ensure all required secrets are set in repository settings
5. **Documentation**: Verify Sphinx configuration and RST file syntax

### Debugging

1. Check workflow logs in the Actions tab
2. Verify environment variables and secrets
3. Test locally with the same configuration
4. Check for missing dependencies or configuration
5. Validate documentation structure and links

## Contributing

When adding new workflows:

1. Follow the existing naming conventions
2. Include proper error handling
3. Add appropriate labels and notifications
4. Update this README with new workflow information
5. Test workflows thoroughly before merging

## Support

For issues with workflows:
1. Check the workflow logs
2. Verify configuration files
3. Test locally first
4. Create an issue with detailed error information