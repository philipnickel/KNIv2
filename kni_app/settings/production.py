from .base import *  # noqa

DEBUG = False

# Static files configuration for production
# Use WhiteNoise's CompressedManifestStaticFilesStorage for optimal performance
# This provides both compression and manifest hashing for cache busting
STORAGES["staticfiles"][
    "BACKEND"
] = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# WhiteNoise manifest strict mode keeps the build honest by failing on missing assets
WHITENOISE_MANIFEST_STRICT = True

# WhiteNoise configuration for production optimization
# Set max age for static files (1 year for immutable files with hashed names)
WHITENOISE_MAX_AGE = 31536000  # 1 year

# Enable static file compression
WHITENOISE_USE_FINDERS = False  # Don't use finders in production for better performance

# Skip compression for files that are already compressed or small
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = [
    "jpg",
    "jpeg",
    "png",
    "gif",
    "webp",
    "zip",
    "gz",
    "tgz",
    "bz2",
    "tbz",
    "xz",
    "br",
    "woff",
    "woff2",
]

# Set Content-Type for common file extensions that might be missing
WHITENOISE_MIMETYPES = {
    ".js.map": "application/json",
    ".css.map": "application/json",
    ".webmanifest": "application/manifest+json",
    ".woff2": "font/woff2",
    ".woff": "font/woff",
}

# Additional static file optimizations
# Serve static files with proper headers
WHITENOISE_ADD_HEADERS_FUNCTION = "whitenoise.middleware.add_headers_function"

# Cache static files for 1 year (since they have hashed names)
WHITENOISE_IMMUTABLE_FILE_TEST = lambda path, url: url.startswith("/static/") and (
    url.endswith(".js")
    or url.endswith(".css")
    or url.endswith(".png")
    or url.endswith(".jpg")
    or url.endswith(".jpeg")
    or url.endswith(".gif")
    or url.endswith(".webp")
    or url.endswith(".svg")
    or url.endswith(".woff")
    or url.endswith(".woff2")
)

# Security configuration

# Ensure that the session cookie is only sent by browsers under an HTTPS connection.
# https://docs.djangoproject.com/en/stable/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True

# Ensure that the CSRF cookie is only sent by browsers under an HTTPS connection.
# https://docs.djangoproject.com/en/stable/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True

# Allow the redirect importer to work in load-balanced / cloud environments.
# https://docs.wagtail.io/en/v2.13/reference/settings.html#redirects
WAGTAIL_REDIRECTS_FILE_STORAGE = "cache"

# Force HTTPS redirect (enabled by default!)
SECURE_SSL_REDIRECT = True

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"
