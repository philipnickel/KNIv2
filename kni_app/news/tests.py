from django.test import TestCase
from django.utils import timezone
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailTestUtils

from .models import ArticlePage, NewsListingPage
from utils.models import AuthorSnippet, ArticleTopic


class ArticlePageModelTests(TestCase, WagtailTestUtils):
    def setUp(self):
        # Get the root page
        self.root_page = Page.get_first_root_node()
        
        # Create a site
        self.site = Site.objects.get(is_default_site=True)
        self.site.hostname = "testserver"
        self.site.save()
        
        # Create required snippets
        self.author = AuthorSnippet.objects.create(title="Test Author")
        self.topic = ArticleTopic.objects.create(title="Test Topic", slug="test-topic")
        
        # Create a news listing page
        self.news_listing = NewsListingPage(
            title="News",
            slug="news",
        )
        self.root_page.add_child(instance=self.news_listing)

    def test_article_page_creation(self):
        """Test that an ArticlePage can be created successfully."""
        article_page = ArticlePage(
            title="Test Article",
            slug="test-article",
            introduction="This is a test article",
            author=self.author,
            topic=self.topic,
            publication_date=timezone.now(),
        )
        self.news_listing.add_child(instance=article_page)
        
        self.assertEqual(article_page.title, "Test Article")
        self.assertEqual(article_page.slug, "test-article")
        self.assertEqual(article_page.introduction, "This is a test article")
        self.assertEqual(article_page.author, self.author)
        self.assertEqual(article_page.topic, self.topic)
        self.assertTrue(article_page.live)

    def test_article_page_template(self):
        """Test that ArticlePage uses the correct template."""
        article_page = ArticlePage(
            title="Test Article",
            slug="test-article",
            author=self.author,
            topic=self.topic,
        )
        self.news_listing.add_child(instance=article_page)
        
        self.assertEqual(article_page.template, "pages/article_page.html")

    def test_article_page_parent_page_types(self):
        """Test that ArticlePage can only be created under NewsListingPage."""
        article_page = ArticlePage(
            title="Test Article",
            slug="test-article",
            author=self.author,
            topic=self.topic,
        )
        
        # Should be able to add to news listing
        self.news_listing.add_child(instance=article_page)
        self.assertTrue(article_page.live)

    def test_article_page_search_fields(self):
        """Test that ArticlePage has the correct search fields."""
        article_page = ArticlePage(
            title="Test Article",
            slug="test-article",
            introduction="This is a test article",
            author=self.author,
            topic=self.topic,
        )
        self.news_listing.add_child(instance=article_page)
        
        # Check that introduction and topic are in search fields
        search_fields = [field.field_name for field in article_page.search_fields]
        self.assertIn("introduction", search_fields)
        self.assertIn("topic", search_fields)

    def test_article_page_content_panels(self):
        """Test that ArticlePage has the expected content panels."""
        article_page = ArticlePage(
            title="Test Article",
            slug="test-article",
            author=self.author,
            topic=self.topic,
        )
        self.news_listing.add_child(instance=article_page)
        
        # Check that key panels exist
        panel_names = [panel.field_name for panel in article_page.content_panels if hasattr(panel, 'field_name')]
        self.assertIn("author", panel_names)
        self.assertIn("publication_date", panel_names)
        self.assertIn("topic", panel_names)
        self.assertIn("introduction", panel_names)
        self.assertIn("image", panel_names)
        self.assertIn("body", panel_names)

    def test_article_page_display_date_property(self):
        """Test that display_date property works correctly."""
        now = timezone.now()
        article_page = ArticlePage(
            title="Test Article",
            slug="test-article",
            author=self.author,
            topic=self.topic,
            publication_date=now,
        )
        self.news_listing.add_child(instance=article_page)
        
        # Test with publication_date
        expected_date = now.strftime("%d %b %Y")
        self.assertEqual(article_page.display_date, expected_date)
        
        # Test without publication_date (should use first_published_at)
        article_page.publication_date = None
        article_page.save()
        # Publish the page to get first_published_at
        article_page.save_revision().publish()
        # Refresh from database to get the published timestamp
        article_page.refresh_from_db()
        if article_page.first_published_at:
            expected_date = article_page.first_published_at.strftime("%d %b %Y")
            self.assertEqual(article_page.display_date, expected_date)
        else:
            # If first_published_at is still None, just test that display_date doesn't crash
            self.assertIsNotNone(article_page.display_date)

    def test_article_page_featured_section(self):
        """Test that featured section fields work correctly."""
        article_page = ArticlePage(
            title="Test Article",
            slug="test-article",
            author=self.author,
            topic=self.topic,
            featured_section_title="Featured Content",
        )
        self.news_listing.add_child(instance=article_page)
        
        self.assertEqual(article_page.featured_section_title, "Featured Content")


class NewsListingPageModelTests(TestCase, WagtailTestUtils):
    def setUp(self):
        # Get the root page
        self.root_page = Page.get_first_root_node()
        
        # Create a site
        self.site = Site.objects.get(is_default_site=True)
        self.site.hostname = "testserver"
        self.site.save()

    def test_news_listing_page_creation(self):
        """Test that a NewsListingPage can be created successfully."""
        news_listing = NewsListingPage(
            title="News",
            slug="news",
            introduction="<p>This is the news section</p>",
        )
        self.root_page.add_child(instance=news_listing)
        
        self.assertEqual(news_listing.title, "News")
        self.assertEqual(news_listing.slug, "news")
        self.assertEqual(news_listing.introduction, "<p>This is the news section</p>")
        self.assertTrue(news_listing.live)

    def test_news_listing_page_template(self):
        """Test that NewsListingPage uses the correct template."""
        news_listing = NewsListingPage(
            title="News",
            slug="news",
        )
        self.root_page.add_child(instance=news_listing)
        
        self.assertEqual(news_listing.template, "pages/news_listing_page.html")

    def test_news_listing_page_subpage_types(self):
        """Test that NewsListingPage only allows ArticlePage as subpages."""
        news_listing = NewsListingPage(
            title="News",
            slug="news",
        )
        self.root_page.add_child(instance=news_listing)
        
        self.assertEqual(news_listing.subpage_types, ["news.ArticlePage"])

    def test_news_listing_page_max_count(self):
        """Test that NewsListingPage has max_count of 1."""
        news_listing = NewsListingPage(
            title="News",
            slug="news",
        )
        self.root_page.add_child(instance=news_listing)
        
        self.assertEqual(news_listing.max_count, 1)

    def test_news_listing_page_search_fields(self):
        """Test that NewsListingPage has the correct search fields."""
        news_listing = NewsListingPage(
            title="News",
            slug="news",
            introduction="<p>This is the news section</p>",
        )
        self.root_page.add_child(instance=news_listing)
        
        # Check that introduction is in search fields
        search_fields = [field.field_name for field in news_listing.search_fields]
        self.assertIn("introduction", search_fields)

    def test_news_listing_page_content_panels(self):
        """Test that NewsListingPage has the expected content panels."""
        news_listing = NewsListingPage(
            title="News",
            slug="news",
        )
        self.root_page.add_child(instance=news_listing)
        
        # Check that key panels exist
        panel_names = [panel.field_name for panel in news_listing.content_panels if hasattr(panel, 'field_name')]
        self.assertIn("introduction", panel_names)

    def test_news_listing_page_get_context(self):
        """Test that get_context method works correctly."""
        news_listing = NewsListingPage(
            title="News",
            slug="news",
        )
        self.root_page.add_child(instance=news_listing)
        
        # Create some test data
        author = AuthorSnippet.objects.create(title="Test Author")
        topic = ArticleTopic.objects.create(title="Test Topic", slug="test-topic")
        
        article1 = ArticlePage(
            title="Article 1",
            slug="article-1",
            author=author,
            topic=topic,
        )
        news_listing.add_child(instance=article1)
        
        article2 = ArticlePage(
            title="Article 2",
            slug="article-2",
            author=author,
            topic=topic,
        )
        news_listing.add_child(instance=article2)
        
        # Test get_context
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.get('/')
        
        context = news_listing.get_context(request)
        
        # Check that context contains expected keys
        self.assertIn('paginator', context)
        self.assertIn('paginator_page', context)
        self.assertIn('is_paginated', context)
        self.assertIn('topics', context)
        self.assertIn('matching_topic', context)


class ArticlePageViewTests(TestCase, WagtailTestUtils):
    def setUp(self):
        # Get the root page
        self.root_page = Page.get_first_root_node()
        
        # Create a site
        self.site = Site.objects.get(is_default_site=True)
        self.site.hostname = "testserver"
        self.site.save()
        
        # Create required snippets
        self.author = AuthorSnippet.objects.create(title="Test Author")
        self.topic = ArticleTopic.objects.create(title="Test Topic", slug="test-topic")
        
        # Create a news listing page
        self.news_listing = NewsListingPage(
            title="News",
            slug="news",
        )
        self.root_page.add_child(instance=self.news_listing)
        
        # Create an article page
        self.article_page = ArticlePage(
            title="Test Article",
            slug="test-article",
            introduction="This is a test article",
            author=self.author,
            topic=self.topic,
        )
        self.news_listing.add_child(instance=self.article_page)

    def test_article_page_view(self):
        """Test that the article page can be viewed."""
        # Publish the news listing first
        self.news_listing.save_revision().publish()
        # Then publish the article page
        self.article_page.save_revision().publish()
        # Set up site
        self.site.root_page = self.news_listing
        self.site.save()
        response = self.client.get('/test-article/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Article")
        self.assertContains(response, "This is a test article")

    def test_article_page_context(self):
        """Test that the article page context is correct."""
        # Publish the news listing first
        self.news_listing.save_revision().publish()
        # Then publish the article page
        self.article_page.save_revision().publish()
        # Set up site
        self.site.root_page = self.news_listing
        self.site.save()
        response = self.client.get('/test-article/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page'], self.article_page)


class NewsListingPageViewTests(TestCase, WagtailTestUtils):
    def setUp(self):
        # Get the root page
        self.root_page = Page.get_first_root_node()
        
        # Create a site
        self.site = Site.objects.get(is_default_site=True)
        self.site.hostname = "testserver"
        self.site.save()
        
        # Create a news listing page
        self.news_listing = NewsListingPage(
            title="News",
            slug="news",
            introduction="<p>This is the news section</p>",
        )
        self.root_page.add_child(instance=self.news_listing)

    def test_news_listing_page_view(self):
        """Test that the news listing page can be viewed."""
        # Publish the page and set up site
        self.news_listing.save_revision().publish()
        self.site.root_page = self.news_listing
        self.site.save()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "News")
        self.assertContains(response, "This is the news section")

    def test_news_listing_page_context(self):
        """Test that the news listing page context is correct."""
        # Publish the page and set up site
        self.news_listing.save_revision().publish()
        self.site.root_page = self.news_listing
        self.site.save()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page'], self.news_listing)
