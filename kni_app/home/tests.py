from django.test import TestCase
from django.urls import reverse
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailTestUtils

from .models import HomePage


class HomePageModelTests(TestCase, WagtailTestUtils):
    def setUp(self):
        # Get the root page
        self.root_page = Page.get_first_root_node()

        # Create a site
        self.site = Site.objects.get(is_default_site=True)
        self.site.hostname = "testserver"
        self.site.save()

    def test_home_page_creation(self):
        """Test that a HomePage can be created successfully."""
        home_page = HomePage(
            title="Test Home Page",
            slug="test-home",
            introduction="This is a test home page",
        )
        self.root_page.add_child(instance=home_page)

        self.assertEqual(home_page.title, "Test Home Page")
        self.assertEqual(home_page.slug, "test-home")
        self.assertEqual(home_page.introduction, "This is a test home page")
        self.assertTrue(home_page.live)

    def test_home_page_template(self):
        """Test that HomePage uses the correct template."""
        home_page = HomePage(
            title="Test Home Page",
            slug="test-home",
        )
        self.root_page.add_child(instance=home_page)

        self.assertEqual(home_page.template, "pages/home_page.html")

    def test_home_page_search_fields(self):
        """Test that HomePage has the correct search fields."""
        home_page = HomePage(
            title="Test Home Page",
            slug="test-home",
            introduction="This is a test home page",
        )
        self.root_page.add_child(instance=home_page)

        # Check that introduction is in search fields
        search_fields = [field.field_name for field in home_page.search_fields]
        self.assertIn("introduction", search_fields)

    def test_home_page_content_panels(self):
        """Test that HomePage has the expected content panels."""
        home_page = HomePage(
            title="Test Home Page",
            slug="test-home",
        )
        self.root_page.add_child(instance=home_page)

        # Check that key panels exist
        panel_names = [
            panel.field_name
            for panel in home_page.content_panels
            if hasattr(panel, "field_name")
        ]
        self.assertIn("introduction", panel_names)
        self.assertIn("hero_cta", panel_names)
        self.assertIn("body", panel_names)

    def test_home_page_hero_cta_streamfield(self):
        """Test that hero_cta StreamField works correctly."""
        home_page = HomePage(
            title="Test Home Page",
            slug="test-home",
        )
        self.root_page.add_child(instance=home_page)

        # Test that hero_cta is a StreamField
        self.assertTrue(hasattr(home_page, "hero_cta"))
        self.assertEqual(len(home_page.hero_cta), 0)

    def test_home_page_featured_section(self):
        """Test that featured section fields work correctly."""
        home_page = HomePage(
            title="Test Home Page",
            slug="test-home",
            featured_section_title="Featured Content",
        )
        self.root_page.add_child(instance=home_page)

        self.assertEqual(home_page.featured_section_title, "Featured Content")

    def test_home_page_inheritance(self):
        """Test that HomePage inherits from BasePage correctly."""
        home_page = HomePage(
            title="Test Home Page",
            slug="test-home",
        )
        self.root_page.add_child(instance=home_page)

        # Test BasePage functionality
        self.assertTrue(hasattr(home_page, "social_image"))
        self.assertTrue(hasattr(home_page, "listing_image"))
        self.assertTrue(hasattr(home_page, "appear_in_search_results"))
        self.assertTrue(home_page.appear_in_search_results)  # Default should be True


class HomePageViewTests(TestCase, WagtailTestUtils):
    def setUp(self):
        # Get the root page
        self.root_page = Page.get_first_root_node()

        # Create a site
        self.site = Site.objects.get(is_default_site=True)
        self.site.hostname = "testserver"
        self.site.save()

        # Create a home page
        self.home_page = HomePage(
            title="Test Home Page",
            slug="test-home",
            introduction="This is a test home page",
        )
        self.root_page.add_child(instance=self.home_page)
        self.site.root_page = self.home_page
        self.site.save()

    def test_home_page_view(self):
        """Test that the home page can be viewed."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Home Page")
        self.assertContains(response, "This is a test home page")

    def test_home_page_context(self):
        """Test that the home page context is correct."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page"], self.home_page)
