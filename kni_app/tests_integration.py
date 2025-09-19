"""
Integration tests for the KNI application.
These tests verify that different components work together correctly.
"""

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from home.models import HomePage
from news.models import ArticlePage, NewsListingPage
from standardpages.models import IndexPage, StandardPage
from utils.models import (
    ArticleTopic,
    AuthorSnippet,
    SocialMediaSettings,
    SystemMessagesSettings,
)
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailTestUtils


class SiteIntegrationTests(TestCase, WagtailTestUtils):
    """Test that the site structure works correctly."""

    def setUp(self):
        # Get the root page
        self.root_page = Page.get_first_root_node()

        # Create a site
        self.site = Site.objects.get(is_default_site=True)
        self.site.hostname = "testserver"
        self.site.save()

        # Create a client
        self.client = Client()

    def test_site_structure_creation(self):
        """Test that we can create a complete site structure."""
        # Create home page
        home_page = HomePage(
            title="Home",
            slug="home-structure",
            introduction="Welcome to our site",
        )
        self.root_page.add_child(instance=home_page)
        self.site.root_page = home_page
        self.site.save()

        # Create standard pages
        about_page = StandardPage(
            title="About",
            slug="about",
            introduction="Learn about us",
        )
        home_page.add_child(instance=about_page)

        contact_page = StandardPage(
            title="Contact",
            slug="contact",
            introduction="Get in touch",
        )
        home_page.add_child(instance=contact_page)

        # Create news section
        news_listing = NewsListingPage(
            title="News",
            slug="news",
            introduction="<p>Latest news and updates</p>",
        )
        home_page.add_child(instance=news_listing)

        # Create index page
        services_index = IndexPage(
            title="Services",
            slug="services",
            introduction="<p>Our services</p>",
        )
        home_page.add_child(instance=services_index)

        # Verify all pages exist
        self.assertTrue(HomePage.objects.filter(slug="home-structure").exists())
        self.assertTrue(StandardPage.objects.filter(slug="about").exists())
        self.assertTrue(StandardPage.objects.filter(slug="contact").exists())
        self.assertTrue(NewsListingPage.objects.filter(slug="news").exists())
        self.assertTrue(IndexPage.objects.filter(slug="services").exists())

    def test_page_navigation(self):
        """Test that page navigation works correctly."""
        # Create home page
        home_page = HomePage(
            title="Home",
            slug="home-nav",
            introduction="Welcome to our site",
        )
        self.root_page.add_child(instance=home_page)
        self.site.root_page = home_page
        self.site.save()

        # Create child pages
        about_page = StandardPage(
            title="About",
            slug="about",
            introduction="Learn about us",
        )
        home_page.add_child(instance=about_page)

        # Test navigation
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About")
        self.assertContains(response, "Learn about us")

    def test_news_section_integration(self):
        """Test that the news section works correctly."""
        # Create home page
        home_page = HomePage(
            title="Home",
            slug="home-news",
        )
        self.root_page.add_child(instance=home_page)
        self.site.root_page = home_page
        self.site.save()

        # Create news listing
        news_listing = NewsListingPage(
            title="News",
            slug="news",
            introduction="<p>Latest news</p>",
        )
        home_page.add_child(instance=news_listing)

        # Create author and topic
        author = AuthorSnippet.objects.create(title="Test Author")
        topic = ArticleTopic.objects.create(title="Technology", slug="technology")

        # Create articles
        article1 = ArticlePage(
            title="First Article",
            slug="first-article",
            introduction="This is the first article",
            author=author,
            topic=topic,
            publication_date=timezone.now(),
        )
        news_listing.add_child(instance=article1)

        article2 = ArticlePage(
            title="Second Article",
            slug="second-article",
            introduction="This is the second article",
            author=author,
            topic=topic,
        )
        news_listing.add_child(instance=article2)

        # Test news listing page
        response = self.client.get("/news/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "News")
        self.assertContains(response, "Latest news")

        # Test individual article pages
        response = self.client.get("/news/first-article/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "First Article")
        self.assertContains(response, "This is the first article")

        response = self.client.get("/news/second-article/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Second Article")
        self.assertContains(response, "This is the second article")

    def test_search_integration(self):
        """Test that search functionality works with content."""
        # Create home page
        home_page = HomePage(
            title="Home",
            slug="home-search",
            introduction="Welcome to our site",
        )
        self.root_page.add_child(instance=home_page)
        self.site.root_page = home_page
        self.site.save()

        # Create content pages
        about_page = StandardPage(
            title="About Us",
            slug="about",
            introduction="We are a technology company",
        )
        home_page.add_child(instance=about_page)

        # Test search
        response = self.client.get("/search/", {"query": "technology"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Search")

        # Test search with no results
        response = self.client.get("/search/", {"query": "nonexistent"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no matching results")

    def test_snippets_integration(self):
        """Test that snippets work correctly with pages."""
        # Create author and topic
        author = AuthorSnippet.objects.create(title="John Doe")
        topic = ArticleTopic.objects.create(title="Science", slug="science")

        # Create home page
        home_page = HomePage(
            title="Home",
            slug="home-snippets",
        )
        self.root_page.add_child(instance=home_page)
        self.site.root_page = home_page
        self.site.save()

        # Create news listing
        news_listing = NewsListingPage(
            title="News",
            slug="news",
        )
        home_page.add_child(instance=news_listing)

        # Create article with snippets
        article = ArticlePage(
            title="Science Article",
            slug="science-article",
            introduction="A fascinating science article",
            author=author,
            topic=topic,
        )
        news_listing.add_child(instance=article)

        # Test that snippets are correctly associated
        self.assertEqual(article.author, author)
        self.assertEqual(article.topic, topic)

        # Test article display
        response = self.client.get("/news/science-article/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Science Article")
        self.assertContains(response, "A fascinating science article")

    def test_settings_integration(self):
        """Test that site settings work correctly."""
        # Create social media settings
        social_settings = SocialMediaSettings.objects.create(
            site=self.site,
            twitter_handle="testuser",
            linkedin_handle="testuser",
            default_sharing_text="Check this out!",
        )

        # Create system messages settings
        system_settings = SystemMessagesSettings.objects.create(
            site=self.site,
            title_404="Custom 404",
            body_404="<p>Page not found</p>",
            footer_newsletter_signup_title="Newsletter",
        )

        # Verify settings exist
        self.assertEqual(social_settings.twitter_handle, "testuser")
        self.assertEqual(system_settings.title_404, "Custom 404")

        # Test that settings can be retrieved
        social_settings = SocialMediaSettings.objects.first()
        system_settings = SystemMessagesSettings.objects.first()

        self.assertIsNotNone(social_settings)
        self.assertIsNotNone(system_settings)

    def test_page_relationships(self):
        """Test that page relationships work correctly."""
        # Create home page
        home_page = HomePage(
            title="Home",
            slug="home-relationships",
        )
        self.root_page.add_child(instance=home_page)
        self.site.root_page = home_page
        self.site.save()

        # Create related pages
        page1 = StandardPage(
            title="Page 1",
            slug="page-1",
        )
        home_page.add_child(instance=page1)

        page2 = StandardPage(
            title="Page 2",
            slug="page-2",
        )
        home_page.add_child(instance=page2)

        # Test page relationships
        self.assertEqual(home_page.get_children().count(), 2)
        self.assertEqual(page1.get_parent(), home_page)
        self.assertEqual(page2.get_parent(), home_page)

        # Test page URLs
        response = self.client.get("/page-1/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/page-2/")
        self.assertEqual(response.status_code, 200)

    def test_content_management_workflow(self):
        """Test a complete content management workflow."""
        # Create home page
        home_page = HomePage(
            title="Home",
            slug="home-workflow",
            introduction="Welcome to our site",
        )
        self.root_page.add_child(instance=home_page)
        self.site.root_page = home_page
        self.site.save()

        # Create author and topic
        author = AuthorSnippet.objects.create(title="Content Manager")
        topic = ArticleTopic.objects.create(title="Updates", slug="updates")

        # Create news section
        news_listing = NewsListingPage(
            title="News",
            slug="news",
            introduction="<p>Latest updates</p>",
        )
        home_page.add_child(instance=news_listing)

        # Create article
        article = ArticlePage(
            title="Important Update",
            slug="important-update",
            introduction="This is an important update",
            author=author,
            topic=topic,
            publication_date=timezone.now(),
        )
        news_listing.add_child(instance=article)

        # Test complete workflow
        # 1. Home page loads
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        # 2. News listing loads
        response = self.client.get("/news/")
        self.assertEqual(response.status_code, 200)

        # 3. Article loads
        response = self.client.get("/news/important-update/")
        self.assertEqual(response.status_code, 200)

        # 4. Search works
        response = self.client.get("/search/?q=update")
        self.assertEqual(response.status_code, 200)

        # 5. All content is properly linked
        self.assertEqual(article.get_parent(), news_listing)
        self.assertEqual(news_listing.get_parent(), home_page)
        self.assertEqual(article.author, author)
        self.assertEqual(article.topic, topic)
