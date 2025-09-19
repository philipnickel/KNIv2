"""
Test settings for the KNI project.
"""

import os
from .base import *  # noqa

# Use SQLite for testing (faster and no setup required)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable migrations for faster tests (optional)
# MIGRATION_MODULES = {
#     'auth': None,
#     'contenttypes': None,
#     'sessions': None,
#     'wagtailcore': None,
#     'wagtailusers': None,
#     'wagtailimages': None,
#     'wagtaildocs': None,
#     'wagtailsearch': None,
#     'wagtailadmin': None,
#     'wagtail': None,
#     'modelcluster': None,
#     'taggit': None,
# }

# Disable debug toolbar
DEBUG = False

# Use in-memory cache for testing
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Disable logging during tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
        'wagtail': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
    },
}

# Use faster password hasher for tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable email sending during tests
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Use a test media root
MEDIA_ROOT = os.path.join(BASE_DIR, 'test-media')

# Disable static files collection during tests
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Test-specific settings
SECRET_KEY = 'test-secret-key-for-ci'

# Disable Wagtail's search backend for tests
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.database',
    }
}

# Use a test site
WAGTAIL_SITE_NAME = 'KNI Test Site'

# Disable file uploads during tests
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024  # 1MB

# Test-specific middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

# Disable external services
WAGTAILIMAGES_EXTENSIONS = ['gif', 'jpg', 'jpeg', 'png', 'webp', 'svg']

# Test-specific timezone
TIME_ZONE = 'UTC'

# Disable internationalization for tests
USE_I18N = False
USE_L10N = False
USE_TZ = True
