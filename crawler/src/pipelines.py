import re
import unicodedata
from datetime import date
from pathlib import Path

import yaml
from itemadapter import ItemAdapter


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
