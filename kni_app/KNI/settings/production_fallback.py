"""
Fallback production settings for troubleshooting static file issues.
Use this configuration if the main production settings fail with static file errors.

To use: Set DJANGO_SETTINGS_MODULE=KNI.settings.production_fallback
"""
from .base import *  # noqa

DEBUG = False

# Use WhiteNoise's basic ManifestStaticFilesStorage instead of compressed version
# This reduces complexity and potential points of failure during deployment
STORAGES["staticfiles"]["BACKEND"] = "whitenoise.storage.ManifestStaticFilesStorage"

# WhiteNoise configuration for reliability over performance
WHITENOISE_USE_FINDERS = False
WHITENOISE_MANIFEST_STRICT = False  # Allow missing files without failing

# Disable static file compression to avoid potential issues
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = [
    'jpg', 'jpeg', 'png', 'gif', 'webp', 'zip', 'gz', 'tgz',
    'bz2', 'tbz', 'xz', 'br', 'woff', 'woff2', 'ico', 'svg',
    'css', 'js'  # Skip compression for CSS/JS as well
]

# Security configuration
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
WAGTAIL_REDIRECTS_FILE_STORAGE = "cache"
SECURE_SSL_REDIRECT = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"

# Add additional logging for static files debugging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s][%(process)d][%(levelname)s][%(name)s] %(message)s"
        }
    },
    "loggers": {
        "KNI": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "wagtail": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.contrib.staticfiles": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "whitenoise": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}