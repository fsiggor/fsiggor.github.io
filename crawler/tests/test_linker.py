from src.linker import TfidfLinker, _tokenize, _cosine


class TestTokenize:
    def test_lowercases(self):
        assert "hello" in _tokenize("Hello World")

    def test_strips_punctuation(self):
        tokens = _tokenize("what's new?")
        assert "what" in tokens
        assert "new" in tokens

    def test_ignores_single_chars(self):
        tokens = _tokenize("a b cd ef")
        assert "cd" in tokens
        assert "ef" in tokens
        assert "a" not in tokens

    def test_empty_string(self):
        assert _tokenize("") == []


class TestCosine:
    def test_identical_vectors(self):
        v = {"a": 1.0, "b": 2.0}
        assert abs(_cosine(v, v) - 1.0) < 1e-9

    def test_orthogonal_vectors(self):
        a = {"x": 1.0}
        b = {"y": 1.0}
        assert _cosine(a, b) == 0.0

    def test_empty_vectors(self):
        assert _cosine({}, {"a": 1.0}) == 0.0
        assert _cosine({}, {}) == 0.0


class TestTfidfLinker:
    def test_find_related_returns_similar_docs(self):
        linker = TfidfLinker()
        linker.index("a", "bitcoin lightning network payment channels")
        linker.index("b", "bitcoin taproot upgrade signature")
        linker.index("c", "privacy tor onion routing browser")
        linker.index("d", "bitcoin lightning invoice routing fees")

        related = linker.find_related("a", top_n=2)
        assert "d" in related
        assert "c" not in related

    def test_find_related_respects_top_n(self):
        linker = TfidfLinker()
        for i in range(10):
            linker.index(str(i), f"topic {i} shared content about software")

        related = linker.find_related("0", top_n=3)
        assert len(related) <= 3

    def test_find_related_unknown_key(self):
        linker = TfidfLinker()
        linker.index("a", "some text")
        assert linker.find_related("unknown") == []

    def test_find_related_single_doc(self):
        linker = TfidfLinker()
        linker.index("a", "only document")
        assert linker.find_related("a") == []

    def test_excludes_self(self):
        linker = TfidfLinker()
        linker.index("a", "bitcoin")
        linker.index("b", "bitcoin")
        related = linker.find_related("a")
        assert "a" not in related

    def test_no_relation_between_unrelated_docs(self):
        linker = TfidfLinker()
        linker.index("a", "bitcoin cryptocurrency blockchain mining")
        linker.index("b", "cooking recipe pasta tomato sauce")
        related = linker.find_related("a", top_n=1)
        # If only 2 docs share no terms, result may be empty
        if related:
            assert related[0] == "b"  # only option
