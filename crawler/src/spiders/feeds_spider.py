"""Spider that fetches RSS feeds and crawls sites for older posts.

Reads sources from sources.json and processes all feeds with a single command.

Usage:
    uv run scrapy crawl feeds
    uv run scrapy crawl feeds -a max_pages=10
"""

from datetime import date
from pathlib import Path

import scrapy
from scrapy.http import Request

from src.config import load_sources
from src.items import PageItem


class FeedsSpider(scrapy.Spider):
    name = "feeds"

    def __init__(self, max_pages=20, domain="inbox", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_pages_per_site = int(max_pages)
        self.domain = domain
        self.pages_per_site = {}

    def start_requests(self):
        sources = load_sources()
        self.logger.info(f"Loaded {len(sources)} sources")

        for source in sources:
            meta = {
                "source_name": source["name"],
                "site_url": source.get("site", ""),
            }
            # Fetch RSS feed
            yield Request(
                url=source["feed"],
                callback=self.parse_feed,
                meta=meta,
                errback=self.handle_error,
                dont_filter=True,
            )
            # Crawl the site for older posts not in the feed
            if source["site"]:
                yield Request(
                    url=source["site"],
                    callback=self.parse_page,
                    meta=meta,
                    errback=self.handle_error,
                )

    def parse_feed(self, response):
        import feedparser

        feed = feedparser.parse(response.text)
        domain = self.domain
        site_key = response.meta.get("site_url") or response.url
        count = 0

        for entry in feed.entries:
            if count >= self.max_pages_per_site:
                break

            title = entry.get("title", "").strip()
            if not title:
                continue

            link = entry.get("link", "")
            summary = entry.get("summary", entry.get("description", ""))
            content = self._feed_content(entry) or summary

            published = entry.get("published_parsed") or entry.get("updated_parsed")
            if published:
                entry_date = date(published.tm_year, published.tm_mon, published.tm_mday).isoformat()
            else:
                entry_date = date.today().isoformat()

            tags = [t.get("term", "") for t in entry.get("tags", []) if t.get("term")]

            count += 1
            # Share counter with parse_page so both respect the same limit
            self.pages_per_site[site_key] = self.pages_per_site.get(site_key, 0) + 1

            yield PageItem(
                title=title,
                url=link,
                date=entry_date,
                description=summary[:300].strip() if summary else "",
                content=content.strip() if content else "",
                tags=tags,
                domain=domain,
            )

    def parse_page(self, response):
        site_url = response.meta["site_url"]
        domain = self.domain
        site_key = site_url or response.url

        crawled = self.pages_per_site.get(site_key, 0)
        if crawled >= self.max_pages_per_site:
            return

        title = response.css("title::text").get("").strip()
        description = (
            response.css('meta[name="description"]::attr(content)').get("")
            or response.css('meta[property="og:description"]::attr(content)').get("")
        )
        page_date = (
            response.css('meta[property="article:published_time"]::attr(content)').get("")
            or response.css("time::attr(datetime)").get("")
            or date.today().isoformat()
        )
        if page_date and "T" in page_date:
            page_date = page_date.split("T")[0]
        if not page_date or len(page_date) < 10:
            page_date = date.today().isoformat()

        content_el = response.css("article") or response.css("main") or response.css("body")
        content = self._extract_markdown(content_el[0]) if content_el else ""

        if len(content.strip()) > 100:
            self.pages_per_site[site_key] = crawled + 1
            yield PageItem(
                title=title,
                url=response.url,
                date=page_date,
                description=description.strip() if description else "",
                content=content.strip(),
                tags=[],
                domain=domain,
            )

        if self.pages_per_site.get(site_key, 0) < self.max_pages_per_site:
            for href in response.css("a::attr(href)").getall():
                yield response.follow(
                    href,
                    callback=self.parse_page,
                    meta=response.meta,
                    errback=self.handle_error,
                )

    def _feed_content(self, entry):
        if hasattr(entry, "content") and entry.content:
            return entry.content[0].get("value", "")
        return ""

    def _extract_markdown(self, selector):
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

    def handle_error(self, failure):
        self.logger.warning(f"Failed: {failure.request.url} - {failure.value}")
