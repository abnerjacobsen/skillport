import pytest

from skillpod.shared.config import Config


def test_openai_requires_key(monkeypatch):
    """provider=openai without key should fail fast."""
    monkeypatch.delenv("SKILLPOD_OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError):
        Config(embedding_provider="openai")


def test_gemini_requires_key(monkeypatch):
    """provider=gemini without key should fail fast."""
    monkeypatch.delenv("SKILLPOD_GEMINI_API_KEY", raising=False)
    with pytest.raises(ValueError):
        Config(embedding_provider="gemini")
