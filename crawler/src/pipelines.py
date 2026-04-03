import re
import unicodedata
from datetime import date
from pathlib import Path

import yaml
from itemadapter import ItemAdapter

from src.linker import Linker, TfidfLinker


DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii").lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:80]


class MarkdownPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        domain = adapter.get("domain", "general")
        title = adapter.get("title", "Untitled")
        item_date = adapter.get("date", date.today().isoformat())

        output_dir = DATA_DIR / domain
        output_dir.mkdir(parents=True, exist_ok=True)

        slug = slugify(title)
        filename = f"{item_date}-{slug}.md"
        filepath = output_dir / filename

        if filepath.exists():
            return item

        frontmatter = {
            "title": title,
            "url": adapter.get("url", ""),
            "date": item_date,
            "draft": False,
            "tags": adapter.get("tags", []),
            "description": adapter.get("description", ""),
        }

        md = "---\n"
        md += yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False)
        md += "---\n\n"
        md += adapter.get("content", "")
        md += "\n"

        filepath.write_text(md, encoding="utf-8")
        spider.logger.info(f"Saved {filepath}")

        return item


class LinkPipeline:
    """Collects items during the crawl, then writes related links on close.

    Depends on the Linker abstraction (Strategy pattern), defaulting to
    TF-IDF cosine similarity. Swap the strategy by overriding _make_linker.
    """

    def __init__(self, linker: Linker | None = None):
        self.linker = linker or TfidfLinker()
        self._items: dict[str, dict] = {}

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        title = adapter.get("title", "")
        content = adapter.get("content", "")
        url = adapter.get("url", "") or title

        self.linker.index(url, f"{title} {content}")
        self._items[url] = {
            "title": title,
            "date": adapter.get("date", ""),
            "domain": adapter.get("domain", "general"),
        }

        return item

    def close_spider(self, spider):
        updated = 0
        for key, meta in self._items.items():
            related_keys = self.linker.find_related(key, top_n=5)
            if not related_keys:
                continue

            filepath = self._resolve_path(meta)
            if not filepath.exists():
                continue

            related_titles = [
                self._items[k]["title"]
                for k in related_keys
                if k in self._items
            ]
            if related_titles:
                _append_wikilinks(filepath, related_titles)
                updated += 1

        spider.logger.info(f"Updated {updated} files with related links")

    def _resolve_path(self, meta: dict) -> Path:
        slug = slugify(meta["title"])
        filename = f"{meta['date']}-{slug}.md"
        return DATA_DIR / meta["domain"] / filename


def _append_wikilinks(filepath: Path, related: list[str]) -> None:
    raw = filepath.read_text(encoding="utf-8")

    # Remove existing related section if re-running
    marker = "\n---\n\n## Related\n"
    if marker in raw:
        raw = raw[:raw.index(marker)]

    links = "\n".join(f"- [[{title}]]" for title in related)
    raw = raw.rstrip("\n") + f"\n\n---\n\n## Related\n\n{links}\n"

    filepath.write_text(raw, encoding="utf-8")
