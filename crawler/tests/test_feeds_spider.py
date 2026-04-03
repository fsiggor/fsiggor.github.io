from datetime import date
from unittest.mock import patch

import pytest
from scrapy.http import HtmlResponse, Request, TextResponse

from src.items import PageItem
from src.spiders.feeds_spider import FeedsSpider


SAMPLE_SOURCES = [
    {"name": "Blog A", "feed": "https://a.com/feed.xml", "site": "https://a.com/"},
    {"name": "Blog B", "feed": "https://b.com/rss", "site": ""},
]

RSS_FEED = """\
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
    <title>Blog A</title>
    <item>
        <title>First Post</title>
        <link>https://a.com/first</link>
        <description>First post description</description>
        <pubDate>Wed, 01 Jan 2026 12:00:00 GMT</pubDate>
    </item>
    <item>
        <title>Second Post</title>
        <link>https://a.com/second</link>
        <description>Second post description</description>
        <pubDate>Thu, 02 Jan 2026 12:00:00 GMT</pubDate>
    </item>
</channel>
</rss>
"""

ATOM_FEED = """\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    <title>Blog B</title>
    <entry>
        <title>Atom Post</title>
        <link href="https://b.com/atom-post"/>
        <summary>Atom summary</summary>
        <updated>2026-03-10T08:00:00Z</updated>
    </entry>
</feed>
"""

ARTICLE_HTML = """\
<html>
<head>
    <title>Test Page</title>
    <meta name="description" content="A test page">
    <meta property="article:published_time" content="2026-02-15T10:00:00Z">
</head>
<body>
    <article>
        <h1>Test Page</h1>
        <p>This is a page with enough content to pass the minimum length check in the spider parser.</p>
        <p>Another paragraph with more details to ensure we exceed the 100 character threshold easily.</p>
    </article>
    <a href="/other">Other page</a>
</body>
</html>
"""

SHORT_HTML = """\
<html><head><title>Short</title></head><body><p>Tiny.</p></body></html>
"""


def fake_text_response(url, body, meta=None):
    request = Request(url=url)
    if meta:
        request = request.replace(meta=meta)
    return TextResponse(url=url, request=request, body=body, encoding="utf-8")


def fake_html_response(url, body, meta=None):
    request = Request(url=url)
    if meta:
        request = request.replace(meta=meta)
    return HtmlResponse(url=url, request=request, body=body, encoding="utf-8")


@pytest.fixture
def spider():
    with patch("src.spiders.feeds_spider.load_sources", return_value=SAMPLE_SOURCES):
        return FeedsSpider()


class TestFeedsSpiderInit:
    def test_default_max_pages(self, spider):
        assert spider.max_pages_per_site == 20

    def test_custom_max_pages(self):
        with patch("src.spiders.feeds_spider.load_sources", return_value=[]):
            s = FeedsSpider(max_pages="5")
        assert s.max_pages_per_site == 5

    def test_default_domain(self, spider):
        assert spider.domain == "general"

    def test_custom_domain(self):
        with patch("src.spiders.feeds_spider.load_sources", return_value=[]):
            s = FeedsSpider(domain="ENG")
        assert s.domain == "ENG"


class TestStartRequests:
    def test_generates_feed_and_site_requests(self, spider):
        with patch("src.spiders.feeds_spider.load_sources", return_value=SAMPLE_SOURCES):
            requests = list(spider.start_requests())
        urls = [r.url for r in requests]
        assert "https://a.com/feed.xml" in urls
        assert "https://a.com/" in urls

    def test_skips_site_crawl_when_no_site_url(self, spider):
        with patch("src.spiders.feeds_spider.load_sources", return_value=SAMPLE_SOURCES):
            requests = list(spider.start_requests())
        urls = [r.url for r in requests]
        assert "https://b.com/rss" in urls
        assert "https://b.com/" not in urls

    def test_feed_request_uses_parse_feed(self, spider):
        with patch("src.spiders.feeds_spider.load_sources", return_value=SAMPLE_SOURCES):
            requests = list(spider.start_requests())
        feed_req = [r for r in requests if "feed.xml" in r.url][0]
        assert feed_req.callback == spider.parse_feed

    def test_site_request_uses_parse_page(self, spider):
        with patch("src.spiders.feeds_spider.load_sources", return_value=SAMPLE_SOURCES):
            requests = list(spider.start_requests())
        site_req = [r for r in requests if r.url == "https://a.com/"][0]
        assert site_req.callback == spider.parse_page

    def test_meta_includes_source_name(self, spider):
        with patch("src.spiders.feeds_spider.load_sources", return_value=SAMPLE_SOURCES):
            requests = list(spider.start_requests())
        assert requests[0].meta["source_name"] == "Blog A"


class TestParseFeed:
    def test_extracts_rss_items(self, spider):
        meta = {"source_name": "Blog A", "site_url": "https://a.com/"}
        response = fake_text_response("https://a.com/feed.xml", RSS_FEED, meta=meta)
        items = list(spider.parse_feed(response))
        assert len(items) == 2

    def test_extracts_title(self, spider):
        meta = {"source_name": "Blog A", "site_url": "https://a.com/"}
        response = fake_text_response("https://a.com/feed.xml", RSS_FEED, meta=meta)
        items = list(spider.parse_feed(response))
        assert items[0]["title"] == "First Post"

    def test_extracts_date(self, spider):
        meta = {"source_name": "Blog A", "site_url": "https://a.com/"}
        response = fake_text_response("https://a.com/feed.xml", RSS_FEED, meta=meta)
        items = list(spider.parse_feed(response))
        assert items[0]["date"] == "2026-01-01"

    def test_extracts_description(self, spider):
        meta = {"source_name": "Blog A", "site_url": "https://a.com/"}
        response = fake_text_response("https://a.com/feed.xml", RSS_FEED, meta=meta)
        items = list(spider.parse_feed(response))
        assert items[0]["description"] == "First post description"

    def test_sets_domain_from_spider(self, spider):
        meta = {"source_name": "Blog A", "site_url": "https://a.com/"}
        response = fake_text_response("https://a.com/feed.xml", RSS_FEED, meta=meta)
        items = list(spider.parse_feed(response))
        assert items[0]["domain"] == "general"

    def test_parses_atom_feed(self, spider):
        meta = {"source_name": "Blog B", "site_url": ""}
        response = fake_text_response("https://b.com/rss", ATOM_FEED, meta=meta)
        items = list(spider.parse_feed(response))
        assert len(items) == 1
        assert items[0]["title"] == "Atom Post"
        assert items[0]["date"] == "2026-03-10"

    def test_skips_entries_without_title(self, spider):
        feed = """\
<?xml version="1.0"?>
<rss version="2.0"><channel><title>T</title>
<item><link>https://a.com/x</link><description>No title here</description></item>
</channel></rss>
"""
        meta = {"source_name": "A", "site_url": ""}
        response = fake_text_response("https://a.com/feed", feed, meta=meta)
        items = list(spider.parse_feed(response))
        assert len(items) == 0

    def test_extracts_tags_from_feed(self, spider):
        feed = """\
<?xml version="1.0"?>
<rss version="2.0"><channel><title>T</title>
<item>
    <title>Tagged Post</title>
    <link>https://a.com/tagged</link>
    <category>python</category>
    <category>web</category>
</item>
</channel></rss>
"""
        meta = {"source_name": "A", "site_url": ""}
        response = fake_text_response("https://a.com/feed", feed, meta=meta)
        items = list(spider.parse_feed(response))
        assert "python" in items[0]["tags"]
        assert "web" in items[0]["tags"]

    def test_respects_max_pages_limit(self):
        with patch("src.spiders.feeds_spider.load_sources", return_value=[]):
            spider = FeedsSpider(max_pages="1")
        meta = {"source_name": "Blog A", "site_url": "https://a.com/"}
        response = fake_text_response("https://a.com/feed.xml", RSS_FEED, meta=meta)
        items = list(spider.parse_feed(response))
        assert len(items) == 1

    def test_shares_counter_with_parse_page(self):
        with patch("src.spiders.feeds_spider.load_sources", return_value=[]):
            spider = FeedsSpider(max_pages="2")
        meta = {"source_name": "Blog A", "site_url": "https://a.com/"}
        response = fake_text_response("https://a.com/feed.xml", RSS_FEED, meta=meta)
        list(spider.parse_feed(response))
        assert spider.pages_per_site["https://a.com/"] == 2


class TestParsePage:
    def test_extracts_page_item(self, spider):
        meta = {"site_url": "https://a.com/", "source_name": "A"}
        response = fake_html_response("https://a.com/post", ARTICLE_HTML, meta=meta)
        items = [i for i in spider.parse_page(response) if not isinstance(i, Request)]
        assert len(items) == 1
        assert items[0]["title"] == "Test Page"
        assert items[0]["domain"] == "general"

    def test_skips_short_content(self, spider):
        meta = {"site_url": "https://a.com/", "source_name": "A"}
        response = fake_html_response("https://a.com/short", SHORT_HTML, meta=meta)
        items = [i for i in spider.parse_page(response) if not isinstance(i, Request)]
        assert len(items) == 0

    def test_respects_max_pages_per_site(self):
        with patch("src.spiders.feeds_spider.load_sources", return_value=[]):
            spider = FeedsSpider(max_pages="1")
        meta = {"site_url": "https://a.com/", "source_name": "A"}

        response1 = fake_html_response("https://a.com/p1", ARTICLE_HTML, meta=meta)
        list(spider.parse_page(response1))
        assert spider.pages_per_site["https://a.com/"] == 1

        response2 = fake_html_response("https://a.com/p2", ARTICLE_HTML, meta=meta)
        items = [i for i in spider.parse_page(response2) if not isinstance(i, Request)]
        assert len(items) == 0

    def test_follows_links(self, spider):
        meta = {"site_url": "https://a.com/", "source_name": "A"}
        response = fake_html_response("https://a.com/post", ARTICLE_HTML, meta=meta)
        results = list(spider.parse_page(response))
        requests = [r for r in results if isinstance(r, Request)]
        assert any("/other" in r.url for r in requests)

    def test_extracts_date_from_meta(self, spider):
        meta = {"site_url": "https://a.com/", "source_name": "A"}
        response = fake_html_response("https://a.com/post", ARTICLE_HTML, meta=meta)
        items = [i for i in spider.parse_page(response) if not isinstance(i, Request)]
        assert items[0]["date"] == "2026-02-15"

    def test_independent_counters_per_site(self):
        with patch("src.spiders.feeds_spider.load_sources", return_value=[]):
            spider = FeedsSpider(max_pages="1")

        meta_a = {"site_url": "https://a.com/", "source_name": "A"}
        meta_b = {"site_url": "https://b.com/", "source_name": "B"}

        resp_a = fake_html_response("https://a.com/p1", ARTICLE_HTML, meta=meta_a)
        resp_b = fake_html_response("https://b.com/p1", ARTICLE_HTML, meta=meta_b)

        items_a = [i for i in spider.parse_page(resp_a) if not isinstance(i, Request)]
        items_b = [i for i in spider.parse_page(resp_b) if not isinstance(i, Request)]

        assert len(items_a) == 1
        assert len(items_b) == 1
