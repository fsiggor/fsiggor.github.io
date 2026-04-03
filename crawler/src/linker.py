"""Linking strategies for finding related documents.

Follows the Strategy pattern — each Linker implementation provides a
different algorithm for computing document similarity.
"""

import math
import re
from abc import ABC, abstractmethod
from collections import Counter


class Linker(ABC):
    """Interface for document linking strategies."""

    @abstractmethod
    def index(self, key: str, text: str) -> None:
        """Add a document to the index."""

    @abstractmethod
    def find_related(self, key: str, top_n: int = 5) -> list[str]:
        """Return keys of the top-N most related documents."""


class TfidfLinker(Linker):
    """Compute document similarity using TF-IDF cosine similarity.

    No external dependencies — uses only Python stdlib.
    """

    def __init__(self):
        self._docs: dict[str, Counter] = {}
        self._df: Counter = Counter()

    def index(self, key: str, text: str) -> None:
        terms = _tokenize(text)
        tf = Counter(terms)
        self._docs[key] = tf
        for term in set(terms):
            self._df[term] += 1

    def find_related(self, key: str, top_n: int = 5) -> list[str]:
        if key not in self._docs:
            return []

        target = self._tfidf(self._docs[key])
        scores = []

        for other_key, other_tf in self._docs.items():
            if other_key == key:
                continue
            score = _cosine(target, self._tfidf(other_tf))
            if score > 0:
                scores.append((other_key, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return [k for k, _ in scores[:top_n]]

    def _tfidf(self, tf: Counter) -> dict[str, float]:
        n = len(self._docs)
        return {
            term: count * math.log(n / self._df[term])
            for term, count in tf.items()
            if self._df[term] > 0
        }


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]{2,}", text.lower())


def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    common = set(a) & set(b)
    if not common:
        return 0.0
    dot = sum(a[t] * b[t] for t in common)
    mag_a = math.sqrt(sum(v * v for v in a.values()))
    mag_b = math.sqrt(sum(v * v for v in b.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)
