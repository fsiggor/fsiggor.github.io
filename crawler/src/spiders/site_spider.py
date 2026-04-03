import scrapy
from datetime import date

from src.items import PageItem


class SiteSpider(scrapy.Spider):
    """Generic spider that crawls a site and extracts page content as markdown.

    Usage:
        uv run scrapy crawl site -a url=https://example.com -a domain=ENG
        uv run scrapy crawl site -a url=https://example.com -a domain=ENG -a max_pages=10
    """

    name = "site"

    def __init__(self, url=None, domain="general", max_pages=50, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not url:
            raise ValueError("Pass -a url=https://...")
        self.start_urls = [url]
        self.domain = domain
        self.max_pages = int(max_pages)
        self.allowed_domains = [url.split("//")[-1].split("/")[0]]
        self.pages_crawled = 0

    def parse(self, response):
        if self.pages_crawled >= self.max_pages:
            return

        # Extract page content
        title = response.css("title::text").get("").strip()
        # Try common meta tags for description
        description = (
            response.css('meta[name="description"]::attr(content)').get("")
            or response.css('meta[property="og:description"]::attr(content)').get("")
        )
        # Try common meta tags for date
        page_date = (
            response.css('meta[property="article:published_time"]::attr(content)').get("")
            or response.css('time::attr(datetime)').get("")
            or date.today().isoformat()
        )
        # Normalize date to YYYY-MM-DD
        if page_date and "T" in page_date:
            page_date = page_date.split("T")[0]
        if not page_date or len(page_date) < 10:
            page_date = date.today().isoformat()

        # Extract main content — try article/main first, fall back to body
        content_el = response.css("article") or response.css("main") or response.css("body")
        if content_el:
            content = self._extract_markdown(content_el[0])
        else:
            content = ""

        # Skip empty or very short pages
        if len(content.strip()) > 100:
            self.pages_crawled += 1
            yield PageItem(
                title=title,
                url=response.url,
                date=page_date,
                description=description.strip(),
                content=content.strip(),
                tags=[],
                domain=self.domain,
            )

        # Follow internal links
        if self.pages_crawled < self.max_pages:
            for href in response.css("a::attr(href)").getall():
                yield response.follow(href, callback=self.parse)

    def _extract_markdown(self, selector):
        """Convert HTML content to simple markdown."""
        parts = []

        for el in selector.css("h1, h2, h3, h4, h5, h6, p, li, pre, blockquote"):
            tag = el.root.tag
            text = el.css("::text").getall()
            text = " ".join(t.strip() for t in text if t.strip())
            if not text:
                continue

            if tag == "h1":
                parts.append(f"# {text}")
            elif tag == "h2":
                parts.append(f"## {text}")
            elif tag == "h3":
                parts.append(f"### {text}")
            elif tag in ("h4", "h5", "h6"):
                parts.append(f"#### {text}")
            elif tag == "li":
                parts.append(f"- {text}")
            elif tag == "pre":
                parts.append(f"```\n{text}\n```")
            elif tag == "blockquote":
                parts.append(f"> {text}")
            else:
                parts.append(text)

        return "\n\n".join(parts)
