"""Tests for the query module."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document

from src.query import search, load_vectorstore


class TestSearch:
    @patch("src.query.load_vectorstore")
    def test_returns_results(self, mock_load):
        mock_store = MagicMock()
        mock_store.similarity_search_with_score.return_value = [
            (Document(page_content="test content", metadata={"source": "test.md"}), 0.85),
        ]
        mock_load.return_value = mock_store

        results = search("test query", k=5)
        assert len(results) == 1
        assert results[0][1] == 0.85

    @patch("src.query.load_vectorstore")
    def test_passes_k_parameter(self, mock_load):
        mock_store = MagicMock()
        mock_store.similarity_search_with_score.return_value = []
        mock_load.return_value = mock_store

        search("test", k=3)
        mock_store.similarity_search_with_score.assert_called_once_with("test", k=3)

    @patch("src.query.load_vectorstore")
    def test_returns_empty_for_no_matches(self, mock_load):
        mock_store = MagicMock()
        mock_store.similarity_search_with_score.return_value = []
        mock_load.return_value = mock_store

        results = search("nonexistent topic")
        assert results == []

    @patch("src.query.load_vectorstore")
    def test_results_contain_metadata(self, mock_load):
        mock_store = MagicMock()
        mock_store.similarity_search_with_score.return_value = [
            (Document(page_content="content", metadata={"source": "path/to/doc.md"}), 0.9),
        ]
        mock_load.return_value = mock_store

        results = search("query")
        doc, score = results[0]
        assert doc.metadata["source"] == "path/to/doc.md"
        assert isinstance(doc.page_content, str)
