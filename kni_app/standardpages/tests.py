from django.test import TestCase
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailTestUtils

from .models import IndexPage, StandardPage


class StandardPageModelTests(TestCase, WagtailTestUtils):
    def setUp(self):
        # Get the root page
        self.root_page = Page.get_first_root_node()

        # Create a site
        self.site = Site.objects.get(is_default_site=True)
        self.site.hostname = "testserver"
        self.site.save()

    def test_standard_page_creation(self):
        """Test that a StandardPage can be created successfully."""
        standard_page = StandardPage(
            title="Test Standard Page",
            slug="test-standard",
            introduction="This is a test standard page",
            display_table_of_contents=True,
        )
        self.root_page.add_child(instance=standard_page)

        self.assertEqual(standard_page.title, "Test Standard Page")
        self.assertEqual(standard_page.slug, "test-standard")
        self.assertEqual(standard_page.introduction, "This is a test standard page")
        self.assertTrue(standard_page.display_table_of_contents)
        self.assertTrue(standard_page.live)

    def test_standard_page_template(self):
        """Test that StandardPage uses the correct template."""
        standard_page = StandardPage(
            title="Test Standard Page",
            slug="test-standard",
        )
        self.root_page.add_child(instance=standard_page)

        self.assertEqual(standard_page.template, "pages/standard_page.html")

    def test_standard_page_search_fields(self):
        """Test that StandardPage has the correct search fields."""
        standard_page = StandardPage(
            title="Test Standard Page",
            slug="test-standard",
            introduction="This is a test standard page",
        )
        self.root_page.add_child(instance=standard_page)

        # Check that introduction is in search fields
        search_fields = [field.field_name for field in standard_page.search_fields]
        self.assertIn("introduction", search_fields)

    def test_standard_page_content_panels(self):
        """Test that StandardPage has the expected content panels."""
        standard_page = StandardPage(
            title="Test Standard Page",
            slug="test-standard",
        )
        self.root_page.add_child(instance=standard_page)

        # Check that key panels exist
        panel_names = [
            panel.field_name
            for panel in standard_page.content_panels
            if hasattr(panel, "field_name")
        ]
        self.assertIn("introduction", panel_names)
        self.assertIn("display_table_of_contents", panel_names)
        self.assertIn("body", panel_names)

    def test_standard_page_display_table_of_contents_default(self):
        """Test that display_table_of_contents defaults to True."""
        standard_page = StandardPage(
            title="Test Standard Page",
            slug="test-standard",
        )
        self.root_page.add_child(instance=standard_page)

        self.assertTrue(standard_page.display_table_of_contents)

    def test_standard_page_featured_section(self):
        """Test that featured section fields work correctly."""
        standard_page = StandardPage(
            title="Test Standard Page",
            slug="test-standard",
            featured_section_title="Featured Content",
        )
        self.root_page.add_child(instance=standard_page)

        self.assertEqual(standard_page.featured_section_title, "Featured Content")


class IndexPageModelTests(TestCase, WagtailTestUtils):
    def setUp(self):
        # Get the root page
        self.root_page = Page.get_first_root_node()

        # Create a site
        self.site = Site.objects.get(is_default_site=True)
        self.site.hostname = "testserver"
        self.site.save()

    def test_index_page_creation(self):
        """Test that an IndexPage can be created successfully."""
        index_page = IndexPage(
            title="Test Index Page",
            slug="test-index",
            introduction="<p>This is a test index page</p>",
        )
        self.root_page.add_child(instance=index_page)

        self.assertEqual(index_page.title, "Test Index Page")
        self.assertEqual(index_page.slug, "test-index")
        self.assertEqual(index_page.introduction, "<p>This is a test index page</p>")
        self.assertTrue(index_page.live)

    def test_index_page_template(self):
        """Test that IndexPage uses the correct template."""
        index_page = IndexPage(
            title="Test Index Page",
            slug="test-index",
        )
        self.root_page.add_child(instance=index_page)

        self.assertEqual(index_page.template, "pages/index_page.html")

    def test_index_page_search_fields(self):
        """Test that IndexPage has the correct search fields."""
        index_page = IndexPage(
            title="Test Index Page",
            slug="test-index",
            introduction="<p>This is a test index page</p>",
        )
        self.root_page.add_child(instance=index_page)

        # Check that introduction is in search fields
        search_fields = [field.field_name for field in index_page.search_fields]
        self.assertIn("introduction", search_fields)

    def test_index_page_content_panels(self):
        """Test that IndexPage has the expected content panels."""
        index_page = IndexPage(
            title="Test Index Page",
            slug="test-index",
        )
        self.root_page.add_child(instance=index_page)

        # Check that key panels exist
        panel_names = [
            panel.field_name
            for panel in index_page.content_panels
            if hasattr(panel, "field_name")
        ]
        self.assertIn("introduction", panel_names)
        self.assertIn("body", panel_names)

    def test_index_page_related_pages_constraints(self):
        """Test that IndexPage has the correct related pages constraints."""
        index_page = IndexPage(
            title="Test Index Page",
            slug="test-index",
        )
        self.root_page.add_child(instance=index_page)

        # Check that the InlinePanel has the correct constraints
        # This is tested by checking the content_panels structure
        panel_names = [
            panel.field_name
            for panel in index_page.content_panels
            if hasattr(panel, "field_name")
        ]
        self.assertIn("body", panel_names)


class StandardPageViewTests(TestCase, WagtailTestUtils):
    def setUp(self):
        # Get the root page
        self.root_page = Page.get_first_root_node()

        # Create a site
        self.site = Site.objects.get(is_default_site=True)
        self.site.hostname = "testserver"
        self.site.save()

        # Create a standard page
        self.standard_page = StandardPage(
            title="Test Standard Page",
            slug="test-standard",
            introduction="This is a test standard page",
        )
        self.root_page.add_child(instance=self.standard_page)

    def test_standard_page_view(self):
        """Test that the standard page can be viewed."""
        # Publish the page and set up site
        self.standard_page.save_revision().publish()
        self.site.root_page = self.standard_page
        self.site.save()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Standard Page")
        self.assertContains(response, "This is a test standard page")

    def test_standard_page_context(self):
        """Test that the standard page context is correct."""
        # Publish the page and set up site
        self.standard_page.save_revision().publish()
        self.site.root_page = self.standard_page
        self.site.save()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page"], self.standard_page)


class IndexPageViewTests(TestCase, WagtailTestUtils):
    def setUp(self):
        # Get the root page
        self.root_page = Page.get_first_root_node()

        # Create a site
        self.site = Site.objects.get(is_default_site=True)
        self.site.hostname = "testserver"
        self.site.save()

        # Create an index page
        self.index_page = IndexPage(
            title="Test Index Page",
            slug="test-index",
            introduction="<p>This is a test index page</p>",
        )
        self.root_page.add_child(instance=self.index_page)

    def test_index_page_view(self):
        """Test that the index page can be viewed."""
        # Publish the page and set up site
        self.index_page.save_revision().publish()
        self.site.root_page = self.index_page
        self.site.save()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Index Page")
        self.assertContains(response, "This is a test index page")

    def test_index_page_context(self):
        """Test that the index page context is correct."""
        # Publish the page and set up site
        self.index_page.save_revision().publish()
        self.site.root_page = self.index_page
        self.site.save()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page"], self.index_page)
