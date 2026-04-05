"""Tests for the ingest module."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document

from src.ingest import load_documents, split_documents, ingest


@pytest.fixture
def sample_docs():
    return [
        Document(
            page_content="---\ntitle: Test Article\ndate: 2026-01-01\n---\n\n# Test Article\n\nThis is a test article about software engineering.",
            metadata={"source": "test1.md"},
        ),
        Document(
            page_content="---\ntitle: Another Article\ndate: 2026-01-02\n---\n\n# Another Article\n\nThis is another test article about flag theory.",
            metadata={"source": "test2.md"},
        ),
    ]


@pytest.fixture
def data_dir(tmp_path):
    inbox = tmp_path / "inbox"
    inbox.mkdir()

    (inbox / "2026-01-01-test-article.md").write_text(
        "---\ntitle: Test Article\ndate: 2026-01-01\n---\n\n# Test Article\n\nThis is a test article.",
        encoding="utf-8",
    )
    (inbox / "2026-01-02-another-article.md").write_text(
        "---\ntitle: Another Article\ndate: 2026-01-02\n---\n\n# Another Article\n\nThis is another article.",
        encoding="utf-8",
    )
    return tmp_path


class TestLoadDocuments:
    def test_loads_markdown_files(self, data_dir):
        docs = load_documents(data_dir)
        assert len(docs) == 2

    def test_returns_empty_for_missing_dir(self, tmp_path):
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        docs = load_documents(empty_dir)
        assert len(docs) == 0

    def test_ignores_non_markdown_files(self, tmp_path):
        (tmp_path / "readme.txt").write_text("not markdown")
        (tmp_path / "doc.md").write_text("# Markdown")
        docs = load_documents(tmp_path)
        assert len(docs) == 1

    def test_loads_nested_directories(self, tmp_path):
        sub = tmp_path / "sub" / "deep"
        sub.mkdir(parents=True)
        (sub / "nested.md").write_text("# Nested")
        (tmp_path / "top.md").write_text("# Top")
        docs = load_documents(tmp_path)
        assert len(docs) == 2


class TestSplitDocuments:
    def test_splits_into_chunks(self, sample_docs):
        chunks = split_documents(sample_docs)
        assert len(chunks) >= len(sample_docs)

    def test_preserves_metadata(self, sample_docs):
        chunks = split_documents(sample_docs)
        sources = {c.metadata["source"] for c in chunks}
        assert "test1.md" in sources
        assert "test2.md" in sources

    def test_respects_chunk_size(self, sample_docs):
        chunks = split_documents(sample_docs)
        for chunk in chunks:
            assert len(chunk.page_content) <= 1200  # chunk_size + overlap margin

    def test_splits_large_document(self):
        large_doc = Document(
            page_content="word " * 500,
            metadata={"source": "large.md"},
        )
        chunks = split_documents([large_doc])
        assert len(chunks) > 1


class TestIngest:
    @patch("src.ingest.create_vectorstore")
    def test_returns_chunk_count(self, mock_vectorstore, data_dir):
        result = ingest(data_dir=data_dir, persist_dir=data_dir / "chroma")
        assert result > 0
        mock_vectorstore.assert_called_once()

    @patch("src.ingest.create_vectorstore")
    def test_returns_zero_for_empty_dir(self, mock_vectorstore, tmp_path):
        empty = tmp_path / "empty"
        empty.mkdir()
        result = ingest(data_dir=empty, persist_dir=tmp_path / "chroma")
        assert result == 0
        mock_vectorstore.assert_not_called()

    @patch("src.ingest.create_vectorstore")
    def test_passes_model_to_vectorstore(self, mock_vectorstore, data_dir):
        ingest(data_dir=data_dir, persist_dir=data_dir / "chroma", model="custom-model")
        args, kwargs = mock_vectorstore.call_args
        # model is the 3rd positional arg
        assert args[2] == "custom-model"
