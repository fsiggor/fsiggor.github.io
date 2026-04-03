# Crawler

Scrapy-based web crawler that scrapes sites and saves each page as a Hugo-compatible markdown file in the `data/` directory at the repo root.

## Setup

```bash
cd crawler
uv sync
```

Requires Python 3.14+ and [uv](https://docs.astral.sh/uv/).

## Usage

```bash
# Crawl a site (saves .md files to data/{domain}/)
uv run scrapy crawl site -a url=https://go.dev/blog -a domain=ENG

# Limit number of pages
uv run scrapy crawl site -a url=https://example.com -a domain=ENG -a max_pages=10
```

### Spider arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `url` | Yes | — | Start URL to crawl |
| `domain` | No | `general` | Subdirectory under `data/` (e.g. `ENG`, `FLAG`, `VIT`) |
| `max_pages` | No | `50` | Maximum number of pages to save |

### Output format

Each scraped page becomes a `.md` file in `data/{domain}/`:

```
data/
└── ENG/
    ├── 2026-04-03-my-article-title.md
    └── 2026-04-03-another-page.md
```

Files have Hugo-compatible YAML frontmatter:

```yaml
---
title: "My Article Title"
url: https://example.com/my-article
date: "2026-04-03"
draft: false
tags: []
description: "Page meta description"
---

# My Article Title

Page content converted to markdown...
```

## Project structure

```
crawler/
├── crawler/
│   ├── spiders/
│   │   └── site_spider.py    # Generic site spider
│   ├── items.py              # PageItem definition
│   ├── pipelines.py          # MarkdownPipeline (writes .md files)
│   ├── settings.py           # Scrapy settings
│   └── middlewares.py        # Default Scrapy middlewares
├── tests/
│   ├── test_spider.py        # Spider parsing and extraction tests
│   └── test_pipelines.py     # Pipeline and slugify tests
├── scrapy.cfg
└── pyproject.toml
```

## How it works

1. **`SiteSpider`** (`site_spider.py`) crawls from the start URL, following internal links up to `max_pages`
2. For each page it extracts: title, description (meta/og:), date (meta/time tag), and body content
3. Body content is converted to markdown (headings, paragraphs, lists, code blocks, blockquotes)
4. Content extraction prefers `<article>`, falls back to `<main>`, then `<body>`
5. Pages with less than 100 characters of content are skipped
6. **`MarkdownPipeline`** (`pipelines.py`) writes each item as a `.md` file with YAML frontmatter
7. Duplicate files (same date + slug) are skipped

## Settings

Key settings in `settings.py`:

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