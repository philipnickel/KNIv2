# Wagtail Compliance Guidelines

## Overview
This document outlines best practices and compliance guidelines for developing with Wagtail CMS, integrating Preline UI components, Docker containerization, and Dokploy deployment strategies.

## Core Wagtail Architecture

### Page-Centric Development
- **Page Models**: All content inherits from `wagtail.models.Page`
- **URL Routing**: Automatic based on page tree hierarchy
- **Template Naming**: Follow snake_case convention (`BlogPage` → `blog_page.html`)
- **Content Structure**: Use StreamField for flexible, mixed-content layouts

### Content Modeling Standards

```python
class BlogPage(Page):
    body = RichTextField()
    date = models.DateField()

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('body')
    ]
```

**Requirements:**
- Implement proper search indexing for all content
- Use content panels for admin interface organization
- Follow StreamField patterns for flexible content

## Preline UI Integration

### Setup Requirements
1. Install Tailwind CSS in Wagtail project
2. Add Preline UI: `npm i preline`
3. Include Preline's JavaScript and styles in base templates
4. Use `w-` prefix for admin interface utilities

### Component Integration Strategy
- Create StreamField blocks using Preline components
- Implement custom page templates with Preline layouts
- Utilize responsive design patterns
- Leverage dark mode variants for enhanced UX

### Template Implementation
```html
<!-- Base template with Preline -->
{% load static %}
<!DOCTYPE html>
<html class="h-full">
<head>
    <link href="{% static 'css/tailwind.css' %}" rel="stylesheet">
    <script src="{% static 'js/preline.js' %}"></script>
</head>
<body class="h-full">
    {% block content %}{% endblock %}
</body>
</html>
```

## Performance Standards

### Caching Requirements
- **Redis**: Implement for fast, persistent caching
- **Template Caching**: Use `{% wagtailcache %}` for fragment caching
- **Image Renditions**: Configure separate cache backends
- **Frontend Proxy**: Implement Varnish or Cloudflare for production

### Database Optimization
- **PostgreSQL**: Required for production deployments
- **Indexing**: Implement proper database indexing strategies
- **Query Optimization**: Follow Django ORM best practices
- **Search**: Consider Elasticsearch for enhanced performance

### Frontend Performance
- Lazy load images with `loading='lazy'` attribute
- Use `{% image_url %}` for efficient image generation
- Implement CDN for static asset delivery
- Optimize bundle sizes with code splitting

## Security Compliance

### Framework Security
- **CSRF Protection**: Implement proper CSRF protection
- **HTTPS**: Enforce HTTPS in production environments
- **Cookies**: Use secure cookie configurations
- **Updates**: Maintain current versions for security patches

### Content Security
- **Rich Text**: Automatic sanitization of rich text content
- **Permissions**: Implement proper permission management
- **User Management**: Use Wagtail's built-in user system
- **Reporting**: Follow security@wagtail.org for vulnerabilities

## Testing Standards

### Required Test Coverage
- Minimum 90% test coverage for all custom code
- Use `WagtailPageTestCase` for page-specific tests
- Test page hierarchy and routing functionality
- Validate admin interface functionality
- Implement StreamField content testing

### Test Implementation
```python
from wagtail.tests.utils import WagtailPageTestCase

class BlogPageTests(WagtailPageTestCase):
    def test_page_creation(self):
        self.assertCanCreateAt(HomePage, BlogPage)
        self.assertPageIsRoutable(self.page)
        self.assertPageIsRenderable(self.page)
```

## Docker Containerization Standards

### Dockerfile Requirements
```dockerfile
FROM python:3.11-slim-buster
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    nodejs \
    npm

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput
```

### Production Configuration
- **Multi-stage builds**: Use for optimized images
- **Health checks**: Configure for container monitoring
- **Volume management**: Proper configuration for media files
- **Gunicorn**: Use with appropriate worker configuration

### Development Workflow
- **Docker Compose**: Required for local development
- **Hot-reload**: Configure for efficient development
- **Environments**: Separate configurations for dev/staging/production
- **Persistence**: Use external volumes for database

## Dokploy Deployment Requirements

### Server Specifications
- **Minimum**: 2GB RAM and 30GB disk space
- **Recommended**: 4GB RAM and 50GB disk space for production
- **CI/CD**: Implement pipelines for production builds
- **Registry**: Use container registry integration (Docker Hub)

### Production Deployment
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  web:
    image: your-registry/wagtail-app:latest
    environment:
      - DATABASE_URL=postgres://user:password@db:5432/wagtail
      - REDIS_URL=redis://redis:6379/0
      - DJANGO_SETTINGS_MODULE=project.settings.production
    volumes:
      - media_files:/app/media
      - static_files:/app/static
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: wagtail
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
  media_files:
  static_files:
```

### Monitoring Requirements
- **Health Checks**: Configure for automatic rollbacks
- **Logging**: Implement centralized logging solutions
- **Backups**: Automated backups for database and media
- **Load Balancing**: Use for high-availability setups

## Project Structure Standards

### Required Directory Structure
```
wagtail_project/
├── apps/
│   ├── blog/
│   ├── home/
│   ├── common/
│   └── __init__.py
├── templates/
│   ├── base.html
│   └── includes/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── media/
├── compose/
│   ├── local.yml
│   └── production.yml
├── requirements/
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
├── Dockerfile
├── docker-compose.yml
└── manage.py
```

### Code Organization
- **Apps**: Modular app-based structure following Django patterns
- **Templates**: Organized by app with shared base templates
- **Static Files**: Separated by type (CSS, JS, images)
- **Requirements**: Split by environment for dependency management

## Wagtail 7.0 Specific Compliance

### New Features Integration
- **Deferred Validation**: Leverage for improved draft workflow
- **Enhanced Pagination**: Implement for large datasets
- **Locale Support**: Use improved internationalization features
- **Django 5.2**: Ensure compatibility with latest Django version

### Migration Requirements
- **Deprecated Features**: Review and update removed features
- **Button Hooks**: Update button rendering hooks
- **Settings**: Rename to new conventions (`TAG_LIMIT` → `WAGTAIL_TAG_LIMIT`)
- **Page Save**: Adapt to new `Page.save()` behavior for drafts

## Development Workflow Standards

### Version Control Requirements
- **Git**: Use semantic commit messages
- **Branching**: Follow GitFlow or GitHub Flow
- **Code Review**: Mandatory for all changes
- **CI/CD**: Automated testing and deployment

### Documentation Standards
- **API Documentation**: Document all custom functionality
- **Code Comments**: Inline documentation for complex logic
- **README**: Comprehensive setup and deployment instructions
- **Changelog**: Maintain version history and breaking changes

### Quality Assurance
- **Linting**: Use flake8, black, and isort for Python
- **Type Checking**: Implement mypy for type safety
- **Pre-commit Hooks**: Automated code quality checks
- **Testing**: Comprehensive test coverage with pytest

## Compliance Checklist

### Pre-deployment Requirements
- [ ] All tests pass with >90% coverage
- [ ] Security scan completed without critical issues
- [ ] Performance benchmarks meet requirements
- [ ] Documentation updated and reviewed
- [ ] Docker images built and tested
- [ ] Database migrations validated
- [ ] Static files collected and optimized
- [ ] Environment variables configured
- [ ] Monitoring and logging configured
- [ ] Backup strategy implemented

### Production Readiness
- [ ] SSL certificates configured
- [ ] Domain name configured
- [ ] CDN setup completed
- [ ] Database backups automated
- [ ] Error monitoring active
- [ ] Performance monitoring active
- [ ] Security headers configured
- [ ] GDPR compliance reviewed
- [ ] Accessibility standards met
- [ ] Load testing completed

## Support and Resources

### Official Documentation
- **Wagtail**: https://docs.wagtail.org/en/7.0/
- **Preline UI**: https://preline.co/docs/
- **Docker**: https://docs.docker.com/
- **Dokploy**: https://dokploy.com/docs/

### Community Resources
- **Wagtail Slack**: Join for community support
- **GitHub Issues**: Report bugs and feature requests
- **Stack Overflow**: Tag questions with wagtail
- **Awesome Wagtail**: Curated list of packages and resources

### Maintenance Schedule
- **Weekly**: Security updates and dependency updates
- **Monthly**: Performance reviews and optimization
- **Quarterly**: Major version updates and feature reviews
- **Annually**: Architecture review and technology stack evaluation