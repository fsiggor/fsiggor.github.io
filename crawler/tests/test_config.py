import json
from pathlib import Path

from src.config import load_sources


SAMPLE_JSON = json.dumps([
    {"name": "Blog A", "feed": "https://a.com/feed.xml", "site": "https://a.com/"},
    {"name": "Blog B", "feed": "https://b.com/rss", "site": "https://b.com/"},
    {"name": "News C", "feed": "https://c.com/atom.xml", "site": ""},
])


class TestLoadSources:
    def test_returns_list(self, tmp_path):
        (tmp_path / "sources.json").write_text(SAMPLE_JSON)
        sources = load_sources(tmp_path / "sources.json")
        assert len(sources) == 3

    def test_extracts_feed_url(self, tmp_path):
        (tmp_path / "sources.json").write_text(SAMPLE_JSON)
        sources = load_sources(tmp_path / "sources.json")
        assert sources[0]["feed"] == "https://a.com/feed.xml"

    def test_extracts_site_url(self, tmp_path):
        (tmp_path / "sources.json").write_text(SAMPLE_JSON)
        sources = load_sources(tmp_path / "sources.json")
        assert sources[0]["site"] == "https://a.com/"

    def test_empty_site_url(self, tmp_path):
        (tmp_path / "sources.json").write_text(SAMPLE_JSON)
        sources = load_sources(tmp_path / "sources.json")
        assert sources[2]["site"] == ""

    def test_extracts_name(self, tmp_path):
        (tmp_path / "sources.json").write_text(SAMPLE_JSON)
        sources = load_sources(tmp_path / "sources.json")
        assert sources[0]["name"] == "Blog A"

    def test_empty_list(self, tmp_path):
        (tmp_path / "sources.json").write_text("[]")
        sources = load_sources(tmp_path / "sources.json")
        assert sources == []

    def test_real_sources_file(self):
        real = Path(__file__).resolve().parents[1] / "sources.json"
        if real.exists():
            sources = load_sources(real)
            assert len(sources) > 40
            assert all(s["feed"] for s in sources)
