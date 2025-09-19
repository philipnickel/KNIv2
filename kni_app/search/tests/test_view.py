from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse
from wagtail.models import Page, Site

from home.models import HomePage


class SearchViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        site = Site.objects.get(is_default_site=True)
        site.hostname = "testserver"
        # Ensure there is a HomePage; create one if missing and set as site root
        home = HomePage.objects.first()
        if home is None:
            root = Page.get_first_root_node()
            # Use a unique slug to avoid conflicts in test DB setup
            home = HomePage(title="Test Home", slug="test-home")
            root.add_child(instance=home)
            home.save_revision().publish()
            site.root_page = home
        site.save()
        cls.home = home
        cls.search_url = reverse("search")

    def test_search_listings_always_return_noindex(self):
        """
        Search pages should apply noindex to avoid Google
        indexing inappropriate search queries.
        For example:
            the query -> example.com/search/?query="buy%20cocaine%20online%20@..."
            should not return -> "Search results for buy cocaine online @...
            on Google.
        """
        unsafe_to_index_search_urls = [
            self.search_url + "?query=illicit",
            self.search_url + "?query=None illicit content",
            self.search_url + "?bar=foo&query=illicit text",
        ]

        for search_url in unsafe_to_index_search_urls:
            with override_settings(SEO_NOINDEX=True):
                resp = self.client.get(search_url)
                # Should contain noindex
                self.assertContains(resp, '<meta name="robots" content="noindex">')
                self.assertEqual(200, resp.status_code)

            # Even with SEO_NOINDEX set to False, the search view should still contain noindex
            with override_settings(SEO_NOINDEX=False):
                resp = self.client.get(search_url)
                # Should contain noindex
                self.assertContains(resp, '<meta name="robots" content="noindex">')
                self.assertEqual(200, resp.status_code)

    def test_search_view_results(self):
        query = self.home.title
        resp = self.client.get(
            self.search_url,
            {"query": query},
            format="json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.home.title)

    def test_search_view_no_results(self):
        resp = self.client.get(
            self.search_url,
            {"query": "gibberish"},
            format="json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "There are no matching results.")
