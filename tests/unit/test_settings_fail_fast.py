import pytest

from skillpod_mcp.config import Settings


def test_c1_openai_requires_key(monkeypatch):
    """WHEN provider=openai and key missing THEN settings init fails (EARS:C1)."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("EMBEDDING_PROVIDER", raising=False)
    with pytest.raises(ValueError):
        Settings(embedding_provider="openai")


def test_c1_gemini_requires_key(monkeypatch):
    """WHEN provider=gemini and key missing THEN settings init fails (EARS:C1)."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("EMBEDDING_PROVIDER", raising=False)
    with pytest.raises(ValueError):
        Settings(embedding_provider="gemini")
