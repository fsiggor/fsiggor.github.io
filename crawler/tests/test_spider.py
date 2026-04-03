from datetime import date

import pytest
from scrapy.http import HtmlResponse, Request

from src.spiders.site_spider import SiteSpider


def fake_response(url, body, status=200):
    request = Request(url=url)
    return HtmlResponse(
        url=url,
        request=request,
        body=body,
        encoding="utf-8",
        status=status,
    )


ARTICLE_HTML = """
<html>
<head>
    <title>Test Article</title>
    <meta name="description" content="A great article about testing">
    <meta property="article:published_time" content="2026-03-15T10:00:00Z">
</head>
<body>
    <article>
        <h1>Test Article</h1>
        <p>This is the first paragraph with enough content to pass the minimum length check for the spider.</p>
        <h2>Section Two</h2>
        <p>Another paragraph here with more details about the topic being discussed in this test article.</p>
    </article>
    <a href="/other-page">Other</a>
</body>
</html>
"""

MINIMAL_HTML = """
<html>
<head><title>Short</title></head>
<body><p>Too short.</p></body>
</html>
"""

NO_ARTICLE_HTML = """
<html>
<head>
    <title>Page With Main</title>
    <meta property="og:description" content="OG description">
</head>
<body>
    <main>
        <h2>Main Content</h2>
        <p>This is content inside a main tag instead of article, with enough text to pass the length threshold.</p>
        <ul>
            <li>Item one</li>
            <li>Item two</li>
        </ul>
    </main>
</body>
</html>
"""

DATE_IN_TIME_TAG_HTML = """
<html>
<head><title>Time Tag Article</title></head>
<body>
    <article>
        <time datetime="2026-01-20">January 20, 2026</time>
        <h1>Time Tag Article</h1>
        <p>Article with date in a time element instead of meta tag, with enough words to pass the threshold.</p>
        <p>Another paragraph to ensure we have enough content for the spider to accept this page.</p>
    </article>
</body>
</html>
"""

CODE_AND_QUOTE_HTML = """
<html>
<head><title>Code Article</title></head>
<body>
    <article>
        <h1>Code Examples</h1>
        <p>Here is an example that shows enough content to pass the length filter in the spider.</p>
        <pre>func main() { fmt.Println("hello") }</pre>
        <blockquote>This is a quote from someone important about programming and software engineering.</blockquote>
        <p>More content to fill the page and make it long enough to be considered valid by the spider.</p>
    </article>
</body>
</html>
"""


class TestSiteSpiderInit:
    def test_requires_url(self):
        with pytest.raises(ValueError, match="Pass -a url"):
            SiteSpider()

    def test_sets_allowed_domains(self):
        spider = SiteSpider(url="https://example.com/blog")
        assert spider.allowed_domains == ["example.com"]

    def test_default_domain(self):
        spider = SiteSpider(url="https://example.com")
        assert spider.domain == "general"

    def test_custom_domain(self):
        spider = SiteSpider(url="https://example.com", domain="ENG")
        assert spider.domain == "ENG"

    def test_max_pages_as_string(self):
        spider = SiteSpider(url="https://example.com", max_pages="5")
        assert spider.max_pages == 5


class TestSiteSpiderParse:
    def setup_method(self):
        self.spider = SiteSpider(url="https://example.com", domain="ENG", max_pages=50)

    def test_extracts_title(self):
        response = fake_response("https://example.com/article", ARTICLE_HTML)
        items = [i for i in self.spider.parse(response) if not isinstance(i, Request)]
        assert items[0]["title"] == "Test Article"

    def test_extracts_meta_description(self):
        response = fake_response("https://example.com/article", ARTICLE_HTML)
        items = [i for i in self.spider.parse(response) if not isinstance(i, Request)]
        assert items[0]["description"] == "A great article about testing"

    def test_extracts_og_description_fallback(self):
        response = fake_response("https://example.com/page", NO_ARTICLE_HTML)
        items = [i for i in self.spider.parse(response) if not isinstance(i, Request)]
        assert items[0]["description"] == "OG description"

    def test_extracts_date_from_meta(self):
        response = fake_response("https://example.com/article", ARTICLE_HTML)
        items = [i for i in self.spider.parse(response) if not isinstance(i, Request)]
        assert items[0]["date"] == "2026-03-15"

    def test_extracts_date_from_time_tag(self):
        response = fake_response("https://example.com/article", DATE_IN_TIME_TAG_HTML)
        items = [i for i in self.spider.parse(response) if not isinstance(i, Request)]
        assert items[0]["date"] == "2026-01-20"

    def test_date_defaults_to_today(self):
        response = fake_response("https://example.com/page", NO_ARTICLE_HTML)
        items = [i for i in self.spider.parse(response) if not isinstance(i, Request)]
        assert items[0]["date"] == date.today().isoformat()

    def test_skips_short_content(self):
        response = fake_response("https://example.com/short", MINIMAL_HTML)
        items = [i for i in self.spider.parse(response) if not isinstance(i, Request)]
        assert len(items) == 0

    def test_follows_links(self):
        response = fake_response("https://example.com/article", ARTICLE_HTML)
        results = list(self.spider.parse(response))
        requests = [r for r in results if isinstance(r, Request)]
        assert any("/other-page" in r.url for r in requests)

    def test_respects_max_pages(self):
        spider = SiteSpider(url="https://example.com", domain="ENG", max_pages=1)
        response = fake_response("https://example.com/article", ARTICLE_HTML)
        list(spider.parse(response))  # first page
        assert spider.pages_crawled == 1
        # Second parse should yield nothing
        response2 = fake_response("https://example.com/other", ARTICLE_HTML)
        items = [i for i in spider.parse(response2) if not isinstance(i, Request)]
        assert len(items) == 0

    def test_sets_domain_on_item(self):
        spider = SiteSpider(url="https://example.com", domain="FLAG")
        response = fake_response("https://example.com/article", ARTICLE_HTML)
        items = [i for i in spider.parse(response) if not isinstance(i, Request)]
        assert items[0]["domain"] == "FLAG"

    def test_uses_main_tag_when_no_article(self):
        response = fake_response("https://example.com/page", NO_ARTICLE_HTML)
        items = [i for i in self.spider.parse(response) if not isinstance(i, Request)]
        assert len(items) == 1
        assert "Main Content" in items[0]["content"]


class TestExtractMarkdown:
    def setup_method(self):
        self.spider = SiteSpider(url="https://example.com", domain="ENG")

    def test_headings(self):
        response = fake_response("https://example.com", ARTICLE_HTML)
        sel = response.css("article")[0]
        md = self.spider._extract_markdown(sel)
        assert "# Test Article" in md
        assert "## Section Two" in md

    def test_paragraphs(self):
        response = fake_response("https://example.com", ARTICLE_HTML)
        sel = response.css("article")[0]
        md = self.spider._extract_markdown(sel)
        assert "first paragraph" in md

    def test_code_blocks(self):
        response = fake_response("https://example.com", CODE_AND_QUOTE_HTML)
        sel = response.css("article")[0]
        md = self.spider._extract_markdown(sel)
        assert "```\nfunc main()" in md

    def test_blockquotes(self):
        response = fake_response("https://example.com", CODE_AND_QUOTE_HTML)
        sel = response.css("article")[0]
        md = self.spider._extract_markdown(sel)
        assert "> This is a quote" in md

    def test_list_items(self):
        response = fake_response("https://example.com", NO_ARTICLE_HTML)
        sel = response.css("main")[0]
        md = self.spider._extract_markdown(sel)
        assert "- Item one" in md
        assert "- Item two" in md
