"""DB package facade.

Exposes SkillDB instance as `db` and re-exports helpers to maintain
backward compatibility with previous `skillhub_mcp.db` module imports.
"""

from ..config import settings  # re-export for legacy patches
from .search import SkillDB, db, lancedb
from .embeddings import get_embedding

__all__ = ["SkillDB", "db", "get_embedding", "lancedb", "settings"]

