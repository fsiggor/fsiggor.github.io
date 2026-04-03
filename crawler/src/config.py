"""Load RSS sources from sources.json."""

import json
from pathlib import Path


SOURCES_PATH = Path(__file__).resolve().parents[1] / "sources.json"


def load_sources(path: Path = SOURCES_PATH) -> list[dict]:
    """Return the list of sources.

    Each dict has: name, feed, site.
    """
    return json.loads(path.read_text())
