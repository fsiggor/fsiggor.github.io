# fsiggor.github.io

Personal blog and landing page of a software engineer. Built with Hugo + Hextra, deployed via GitHub Pages. Includes a Scrapy-based crawler that fetches RSS feeds and scrapes sites, saving content as markdown with Obsidian-compatible `[[wikilinks]]`.

## Repository structure

```
├── blog/                        # Hugo + Hextra site
│   ├── hugo.toml
│   ├── content/
│   ├── archetypes/
│   └── static/
├── crawler/                     # Scrapy RSS crawler
│   ├── src/                     # Spiders, pipelines, linker
│   ├── tests/
│   ├── sources.json             # RSS sources configuration
│   └── pyproject.toml
├── data/                        # Crawled markdown files (gitignored)
├── docs/                        # Project documentation
│   ├── ARCHITECTURE.md
│   ├── GUIDELINES.md
│   ├── CONTRIBUTING.md
│   ├── SECURITY.md
│   ├── SOURCES.md
│   └── PUBLISHING.md
├── AGENTS.md                    # Instructions for AI agents
└── .github/workflows/           # CI/CD
```

## Quick start

### Blog

```bash
cd blog
hugo server -D
```

Site available at http://localhost:1313/.

### Crawler

```bash
cd crawler
uv sync
uv run scrapy crawl feeds
```

Fetches all RSS sources, crawls sites for older posts, saves `.md` files to `data/`, and creates `[[wikilinks]]` between related documents. See [crawler/README.md](crawler/README.md) for details.

## Documentation

| Document | Content |
|----------|---------|
| [AGENTS.md](AGENTS.md) | Instructions for AI agents |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Architecture and pipeline |
| [GUIDELINES.md](docs/GUIDELINES.md) | Content conventions and frontmatter |
| [CONTRIBUTING.md](docs/CONTRIBUTING.md) | How to contribute |
| [SECURITY.md](docs/SECURITY.md) | Security and sensitive data |
| [SOURCES.md](docs/SOURCES.md) | Source catalog by domain |
| [PUBLISHING.md](docs/PUBLISHING.md) | Publishing pipeline |

## License

Personal project — private use.
