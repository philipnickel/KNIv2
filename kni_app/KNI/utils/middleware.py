"""Custom middleware helpers used by the KNI project."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from django.http import HttpRequest, HttpResponse

from wagtail.models import Site


@dataclass
class EnsureSiteMiddleware:
    """Ensure ``request.site`` resolves even for hosts without a Site record.

    Dokploy preview deployments spin up on ephemeral hostnames that are not
    represented in the Wagtail ``Site`` table. ``Site.find_for_request`` returns
    ``None`` in that scenario which ultimately surfaces as a 404 when the
    request reaches the Wagtail router.  Falling back to the configured default
    site (or the first Site in the database) lets us keep serving the preview
    without requiring manual admin updates for every preview hostname.
    """

    get_response: Callable[[HttpRequest], HttpResponse]

    def __call__(self, request: HttpRequest) -> HttpResponse:
        site = Site.find_for_request(request)

        if site is None:
            # Try the configured default site first.
            site = Site.objects.filter(is_default_site=True).select_related("root_page").first()

            # Fallback to the first available site if no default is flagged.
            if site is None:
                site = Site.objects.select_related("root_page").first()

            if site is not None:
                request._wagtail_site = site  # cached attribute used by Wagtail routing

        if site is not None:
            request.site = site

        return self.get_response(request)
