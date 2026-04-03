# Crawler

Scrapy-based crawler that fetches RSS feeds and scrapes sites, saving each page as a Hugo-compatible markdown file in the `data/` directory at the repo root.

## Setup

```bash
cd crawler
uv sync
```

Requires Python 3.14+ and [uv](https://docs.astral.sh/uv/).

## Usage

### Fetch all sources (RSS + site crawl)

```bash
uv run scrapy crawl feeds
```

This reads `sources.json`, fetches every RSS feed, and crawls each site for older posts not covered by the feed. All results are saved as `.md` files to `data/{domain}/`.

```bash
# Limit pages crawled per site (default: 20)
uv run scrapy crawl feeds -a max_pages=5
```

### Crawl a single site

```bash
uv run scrapy crawl site -a url=https://example.com/blog -a domain=ENG
uv run scrapy crawl site -a url=https://example.com -a domain=ENG -a max_pages=10
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `url` | Yes | — | Start URL to crawl |
| `domain` | No | `general` | Subdirectory under `data/` |
| `max_pages` | No | `50` | Maximum pages to save |

## Adding sources

Edit `sources.json`. Each domain key maps to a list of sources:

```json
{
  "bitcoin": [
    {"name": "Bitcoin Optech", "feed": "https://bitcoinops.org/feed.xml", "site": "https://bitcoinops.org/"}
  ]
}
```

| Field | Description |
|-------|-------------|
| `name` | Source display name |
| `feed` | RSS/Atom feed URL |
| `site` | Site URL for crawling older posts (empty string to skip) |

## Output format

```
data/
├── bitcoin/
│   ├── 2026-01-15-bitcoin-optech-newsletter.md
│   └── 2026-02-01-taproot-activation.md
├── privacy/
└── security/
```

Each file has Hugo-compatible YAML frontmatter:

```yaml
---
title: "Bitcoin Optech Newsletter"
url: https://bitcoinops.org/en/newsletters/2026-01-15/
date: "2026-01-15"
draft: false
tags: [bitcoin, newsletter]
description: "Weekly newsletter covering Bitcoin technical developments"
---

Page content in markdown...
```

## Project structure

```
crawler/
├── src/
│   ├── spiders/
│   │   ├── feeds_spider.py   # Multi-source RSS + site crawler
│   │   └── site_spider.py    # Single-site spider
│   ├── config.py             # Loads sources.json
│   ├── items.py              # PageItem definition
│   ├── pipelines.py          # MarkdownPipeline (writes .md files)
│   └── settings.py           # Scrapy settings
├── tests/
│   ├── test_feeds_spider.py  # Feeds spider tests
│   ├── test_spider.py        # Site spider tests
│   ├── test_pipelines.py     # Pipeline and slugify tests
│   └── test_config.py        # Config loading tests
├── sources.json              # RSS sources configuration
├── scrapy.cfg
└── pyproject.toml
```

## How it works

### FeedsSpider (`feeds`)

1. Reads all sources from `sources.json`
2. For each source: fetches the RSS/Atom feed and extracts items (title, date, content, tags)
3. For each source with a `site` URL: crawls the site for older posts (up to `max_pages` per site)
4. **MarkdownPipeline** writes each item as a `.md` file with YAML frontmatter
5. Duplicate files (same date + slug) are skipped

### SiteSpider (`site`)

1. Crawls from a start URL, following internal links up to `max_pages`
2. Extracts title, description (meta/og:), date (meta/time tag), and body content
3. Content extraction prefers `<article>`, falls back to `<main>`, then `<body>`
4. Pages with less than 100 characters of content are skipped

## Settings

- `ROBOTSTXT_OBEY = True` — respects robots.txt
- `CONCURRENT_REQUESTS_PER_DOMAIN = 1` — one request at a time per domain
- `DOWNLOAD_DELAY = 1` — 1 second between requests

## Tests

```bash
uv run pytest tests/ -v
```

## References

- https://docs.scrapy.org/en/latest
- https://www.scrapingbee.com/blog/web-scraping-101-with-python/#common-web-scraping-errors-and-fixes
- https://scrapfly.io/blog/posts/how-to-use-web-scaping-for-rag-applications
