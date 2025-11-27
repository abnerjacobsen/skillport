"""Query-facing public APIs."""

from typing import Dict, List, Optional

from skillpod.shared.config import Config
from ..internal.lancedb import IndexStore


def search(query: str, *, limit: int, config: Config) -> List[Dict]:
    store = IndexStore(config)
    return store.search(query, limit=limit)


def get_by_id(skill_id: str, *, config: Config) -> Optional[Dict]:
    store = IndexStore(config)
    return store.get_by_id(skill_id)


def list_all(*, limit: int, config: Config) -> List[Dict]:
    store = IndexStore(config)
    return store.list_all(limit=limit)
