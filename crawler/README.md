# Crawler

Scrapy-based crawler that fetches RSS feeds and scrapes sites, saving each page as a Hugo-compatible markdown file in the `data/` directory at the repo root. Automatically creates `[[wikilinks]]` between related documents for use in Obsidian.

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

# Set the output domain/folder
uv run scrapy crawl feeds -a domain=bitcoin
```

### Crawl a single site

```bash
uv run scrapy crawl site -a url=https://example.com/blog -a domain=samples
uv run scrapy crawl site -a url=https://example.com -a domain=samples -a max_pages=10
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `url` | Yes | — | Start URL to crawl |
| `domain` | No | `general` | Subdirectory under `data/` |
| `max_pages` | No | `50` | Maximum pages to save |

## Adding sources

Edit `sources.json`. Each entry is an object with:

```json
[
  {"name": "Bitcoin Optech", "feed": "https://bitcoinops.org/feed.xml", "site": "https://bitcoinops.org/"}
]
```

| Field | Description |
|-------|-------------|
| `name` | Source display name |
| `feed` | RSS/Atom feed URL |
| `site` | Site URL for crawling older posts (empty string to skip) |

## Output format

```
data/
└── inbox/
    ├── 2026-01-15-bitcoin-optech-newsletter.md
    └── 2026-02-01-taproot-activation.md
```

Each file has Hugo-compatible YAML frontmatter and Obsidian-compatible wikilinks:

```markdown
---
title: "Bitcoin Optech Newsletter"
url: https://bitcoinops.org/en/newsletters/2026-01-15/
date: "2026-01-15"
draft: false
tags: [bitcoin, newsletter]
description: "Weekly newsletter covering Bitcoin technical developments"
---

Page content in markdown...

---

## Related

- [[Bitcoin Taproot Upgrade]]
- [[Lightning Network Payment Channels]]
```

The `## Related` section with `[[wikilinks]]` is generated automatically using TF-IDF cosine similarity. Obsidian's graph view picks these up as connections between notes.

## How it works

### Pipelines

1. **MarkdownPipeline** (priority 300) — writes each item as a `.md` file with YAML frontmatter. Skips duplicates (same date + slug).
2. **LinkPipeline** (priority 400) — collects all items during the crawl, then on spider close computes TF-IDF similarity and appends `[[wikilinks]]` to each file.

The linking strategy is decoupled via the `Linker` abstraction (Strategy pattern). The default `TfidfLinker` uses cosine similarity with zero external dependencies (stdlib only). New strategies (embeddings, NER, tags) can be swapped in by implementing the `Linker` interface.

### Spiders

- **FeedsSpider** (`feeds`) — reads `sources.json`, fetches RSS/Atom feeds, and crawls sites for older posts. Limits pages per source via `max_pages`.
- **SiteSpider** (`site`) — crawls a single site from a start URL. Extracts content preferring `<article>` > `<main>` > `<body>`.

### Settings

- `CONCURRENT_REQUESTS = 16` — up to 16 requests in flight across all domains
- `CONCURRENT_REQUESTS_PER_DOMAIN = 2` — 2 parallel requests per domain
- `DOWNLOAD_DELAY = 0.5` — base delay between requests (autothrottle adjusts per server)
- `AUTOTHROTTLE_ENABLED = True` — auto-adjusts delay based on server response times
- `AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0` — targets 2 concurrent requests per domain
- `ROBOTSTXT_OBEY = True` — respects robots.txt
- `RETRY_TIMES = 3` — retries on 500, 502, 503, 504, 408, 429
- `DOWNLOAD_TIMEOUT = 30` — fails fast on slow/dead sites
- `DNSCACHE_ENABLED = True` — caches DNS lookups across domains

## Project structure

```
crawler/
├── src/
│   ├── spiders/
│   │   ├── feeds_spider.py   # Multi-source RSS + site crawler
│   │   └── site_spider.py    # Single-site spider
│   ├── config.py             # Loads sources.json
│   ├── items.py              # PageItem definition
│   ├── linker.py             # Linker ABC + TfidfLinker strategy
│   ├── pipelines.py          # MarkdownPipeline + LinkPipeline
│   └── settings.py           # Scrapy settings
├── tests/
│   ├── test_config.py        # Config loading tests
│   ├── test_feeds_spider.py  # Feeds spider tests
│   ├── test_linker.py        # TF-IDF linker tests
│   ├── test_pipelines.py     # Pipeline, slugify, and wikilink tests
│   └── test_spider.py        # Site spider tests
├── sources.json              # RSS sources configuration
├── scrapy.cfg
└── pyproject.toml
```

## Tests

```bash
uv run pytest tests/ -v
```

## References

- https://docs.scrapy.org/en/latest
- https://www.scrapingbee.com/blog/web-scraping-101-with-python/#common-web-scraping-errors-and-fixes
- https://scrapfly.io/blog/posts/how-to-use-web-scaping-for-rag-applications
