import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict

from skillsouko.shared.config import SKILLSOUKO_HOME

ORIGIN_PATH = (SKILLSOUKO_HOME / "meta" / "origins.json").expanduser().resolve()


def _load() -> Dict[str, Any]:
    if not ORIGIN_PATH.exists():
        return {}
    try:
        with open(ORIGIN_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
    except Exception as exc:
        print(f"[WARN] Failed to load origins.json: {exc}", file=sys.stderr)
    return {}


def _save(data: Dict[str, Any]) -> None:
    ORIGIN_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(ORIGIN_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def record_origin(skill_id: str, payload: Dict[str, Any]) -> None:
    data = _load()
    enriched = dict(payload)
    enriched.setdefault("added_at", datetime.now(timezone.utc).isoformat())
    data[skill_id] = enriched
    _save(data)


def remove_origin(skill_id: str) -> None:
    data = _load()
    if skill_id in data:
        del data[skill_id]
        _save(data)
