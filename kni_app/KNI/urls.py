import re

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path, re_path
from django.views.decorators.http import require_http_methods
from django.views.static import serve as serve_static
from search import views as search_views
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls


@require_http_methods(["GET"])
def health_check(request):
    """Health check endpoint for production monitoring"""
    return JsonResponse({"status": "healthy", "service": "kni_app", "version": "1.0.0"})


urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("health/", health_check, name="health_check"),
]


if settings.MEDIA_URL and settings.MEDIA_ROOT:
    # Normalize the media prefix and register explicit serving patterns for production
    media_prefix = settings.MEDIA_URL.lstrip("/")
    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    else:
        urlpatterns += [
            re_path(
                r"^%s(?P<path>.*)$" % re.escape(media_prefix),
                serve_static,
                {"document_root": settings.MEDIA_ROOT},
            ),
        ]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static files from development server
    urlpatterns += staticfiles_urlpatterns()

urlpatterns += [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
