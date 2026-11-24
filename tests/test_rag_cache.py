"""Lightweight test for RAG client caching without loading ML weights."""
import sys
from types import SimpleNamespace

from src.rag import engine


def test_chroma_client_reused(monkeypatch, tmp_path):
    calls = []

    def fake_client(path):
        client = object()
        calls.append((path, client))
        return client

    monkeypatch.setattr(engine, "INDEX_PATH", tmp_path)
    monkeypatch.setitem(sys.modules, "chromadb", SimpleNamespace(PersistentClient=fake_client))
    engine._db.cache_clear()
    try:
        first = engine._db()
        second = engine._db()
        assert first is second
        assert len(calls) == 1
        assert calls[0][0] == str(tmp_path)
    finally:
        engine._db.cache_clear()
