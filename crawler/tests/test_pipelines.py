import logging
from datetime import date
from pathlib import Path

import pytest
import yaml

from src.items import PageItem
from src.linker import TfidfLinker
from src.pipelines import LinkPipeline, MarkdownPipeline, _append_wikilinks, slugify


# --- slugify ---


class TestSlugify:
    def test_basic(self):
        assert slugify("Hello World") == "hello-world"

    def test_special_characters(self):
        assert slugify("What's new in Go 1.22?") == "what-s-new-in-go-1-22"

    def test_accents_stripped(self):
        assert slugify("Análise da Selic março") == "analise-da-selic-marco"

    def test_truncates_at_80_chars(self):
        long_title = "a" * 200
        assert len(slugify(long_title)) == 80

    def test_strips_leading_trailing_hyphens(self):
        assert slugify("---hello---") == "hello"

    def test_empty_string(self):
        assert slugify("") == ""

    def test_unicode_only(self):
        assert slugify("日本語") == ""


# --- MarkdownPipeline ---


class FakeSpider:
    def __init__(self):
        self.logger = logging.getLogger("test")


@pytest.fixture
def output_dir(tmp_path, monkeypatch):
    monkeypatch.setattr("src.pipelines.DATA_DIR", tmp_path)
    return tmp_path


@pytest.fixture
def pipeline():
    return MarkdownPipeline()


@pytest.fixture
def spider():
    return FakeSpider()


def make_item(**overrides):
    defaults = {
        "title": "Test Article",
        "url": "https://example.com/test",
        "date": "2026-04-03",
        "description": "A test article",
        "content": "Some content here.",
        "tags": ["tech", "go"],
        "domain": "ENG",
    }
    defaults.update(overrides)
    return PageItem(**defaults)


class TestMarkdownPipeline:
    def test_creates_file_with_frontmatter(self, pipeline, spider, output_dir):
        item = make_item()
        pipeline.process_item(item, spider)

        files = list((output_dir / "ENG").glob("*.md"))
        assert len(files) == 1

        content = files[0].read_text()
        assert content.startswith("---\n")
        assert "title: Test Article" in content
        assert "url: https://example.com/test" in content
        assert "draft: false" in content

    def test_frontmatter_is_valid_yaml(self, pipeline, spider, output_dir):
        item = make_item()
        pipeline.process_item(item, spider)

        filepath = list((output_dir / "ENG").glob("*.md"))[0]
        raw = filepath.read_text()
        # Extract YAML between --- markers
        parts = raw.split("---")
        frontmatter = yaml.safe_load(parts[1])

        assert frontmatter["title"] == "Test Article"
        assert frontmatter["date"] == "2026-04-03"
        assert frontmatter["tags"] == ["tech", "go"]
        assert frontmatter["draft"] is False

    def test_content_after_frontmatter(self, pipeline, spider, output_dir):
        item = make_item(content="# Hello\n\nWorld")
        pipeline.process_item(item, spider)

        filepath = list((output_dir / "ENG").glob("*.md"))[0]
        raw = filepath.read_text()
        parts = raw.split("---\n")
        body = parts[2]
        assert "# Hello" in body
        assert "World" in body

    def test_filename_format(self, pipeline, spider, output_dir):
        item = make_item(title="My Great Post", date="2026-04-03")
        pipeline.process_item(item, spider)

        files = list((output_dir / "ENG").glob("*.md"))
        assert files[0].name == "2026-04-03-my-great-post.md"

    def test_creates_domain_subdirectory(self, pipeline, spider, output_dir):
        item = make_item(domain="FLAG")
        pipeline.process_item(item, spider)

        assert (output_dir / "FLAG").is_dir()
        assert len(list((output_dir / "FLAG").glob("*.md"))) == 1

    def test_skips_existing_file(self, pipeline, spider, output_dir):
        item = make_item()
        pipeline.process_item(item, spider)
        # Write again — should not overwrite
        filepath = list((output_dir / "ENG").glob("*.md"))[0]
        original_content = filepath.read_text()
        pipeline.process_item(make_item(content="CHANGED"), spider)
        assert filepath.read_text() == original_content

    def test_defaults_for_missing_fields(self, pipeline, spider, output_dir):
        item = PageItem(title="Bare", domain="ENG")
        pipeline.process_item(item, spider)

        filepath = list((output_dir / "ENG").glob("*.md"))[0]
        raw = filepath.read_text()
        parts = raw.split("---")
        fm = yaml.safe_load(parts[1])

        assert fm["url"] == ""
        assert fm["tags"] == []
        assert fm["description"] == ""

    def test_special_chars_in_title(self, pipeline, spider, output_dir):
        item = make_item(title="What's new in C++ & Rust?")
        pipeline.process_item(item, spider)

        files = list((output_dir / "ENG").glob("*.md"))
        assert len(files) == 1
        assert "what-s-new-in-c-rust" in files[0].name

    def test_returns_item(self, pipeline, spider, output_dir):
        item = make_item()
        result = pipeline.process_item(item, spider)
        assert result is item


# --- _append_wikilinks ---


class TestAppendWikilinks:
    def test_adds_related_section_with_wikilinks(self, tmp_path):
        md_file = tmp_path / "test.md"
        md_file.write_text("---\ntitle: Test\n---\n\nContent here.\n")
        _append_wikilinks(md_file, ["Related A", "Related B"])
        raw = md_file.read_text()
        assert "- [[Related A]]" in raw
        assert "- [[Related B]]" in raw

    def test_preserves_body_content(self, tmp_path):
        md_file = tmp_path / "test.md"
        md_file.write_text("---\ntitle: T\n---\n\n# Hello\n\nWorld\n")
        _append_wikilinks(md_file, ["X"])
        raw = md_file.read_text()
        assert "# Hello" in raw
        assert "World" in raw
        assert "- [[X]]" in raw

    def test_related_section_at_end(self, tmp_path):
        md_file = tmp_path / "test.md"
        md_file.write_text("---\ntitle: T\n---\n\nBody.\n")
        _append_wikilinks(md_file, ["A"])
        raw = md_file.read_text()
        assert raw.endswith("- [[A]]\n")

    def test_replaces_existing_related_section(self, tmp_path):
        md_file = tmp_path / "test.md"
        md_file.write_text(
            "---\ntitle: T\n---\n\nBody.\n\n---\n\n## Related\n\n- [[Old]]\n"
        )
        _append_wikilinks(md_file, ["New"])
        raw = md_file.read_text()
        assert "[[Old]]" not in raw
        assert "- [[New]]" in raw
        assert raw.count("## Related") == 1


# --- LinkPipeline ---


class TestLinkPipeline:
    def test_indexes_items(self):
        lp = LinkPipeline()
        item = make_item(title="Bitcoin Post", content="bitcoin lightning network")
        lp.process_item(item, FakeSpider())
        assert len(lp._items) == 1

    def test_returns_item(self):
        lp = LinkPipeline()
        item = make_item()
        result = lp.process_item(item, FakeSpider())
        assert result is item

    def test_accepts_custom_linker(self):
        linker = TfidfLinker()
        lp = LinkPipeline(linker=linker)
        assert lp.linker is linker

    def test_close_spider_updates_files(self, tmp_path, monkeypatch):
        monkeypatch.setattr("src.pipelines.DATA_DIR", tmp_path)

        lp = LinkPipeline()
        spider = FakeSpider()

        items = [
            make_item(
                title="Bitcoin Lightning",
                url="https://example.com/lightning",
                content="bitcoin lightning network payment channels scaling",
            ),
            make_item(
                title="Bitcoin Taproot",
                url="https://example.com/taproot",
                content="bitcoin taproot upgrade schnorr signature",
            ),
            make_item(
                title="Privacy Tor",
                url="https://example.com/tor",
                content="privacy tor onion routing anonymous browsing",
            ),
        ]

        # First write files via MarkdownPipeline
        mp = MarkdownPipeline()
        for item in items:
            mp.process_item(item, spider)

        # Then index in LinkPipeline
        for item in items:
            lp.process_item(item, spider)

        lp.close_spider(spider)

        # Check that at least one file got wikilinks
        md_files = list((tmp_path / "ENG").glob("*.md"))
        any_related = False
        for f in md_files:
            raw = f.read_text()
            if "## Related" in raw and "[[" in raw:
                any_related = True

        assert any_related

    def test_close_spider_skips_missing_files(self):
        lp = LinkPipeline()
        spider = FakeSpider()

        lp.process_item(make_item(title="Ghost", content="this file wont exist"), spider)
        lp.process_item(make_item(title="Ghost 2", content="this file wont exist either"), spider)

        # Should not raise
        lp.close_spider(spider)
