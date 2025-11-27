from __future__ import annotations

from pathlib import Path

from skillsouko.modules.indexing import get_by_id as idx_get_by_id
from skillsouko.shared.config import Config
from skillsouko.shared.exceptions import SkillNotFoundError
from skillsouko.shared.filters import is_skill_enabled
from skillsouko.shared.utils import resolve_inside
from .types import FileContent


def read_skill_file(skill_id: str, file_path: str, *, config: Config) -> FileContent:
    record = idx_get_by_id(skill_id, config=config)
    if not record:
        raise SkillNotFoundError(skill_id)

    identifier = record.get("id", skill_id)
    if not is_skill_enabled(identifier, record.get("category"), config=config):
        raise SkillNotFoundError(identifier)

    skill_dir = Path(record.get("path", "")).resolve()
    target = resolve_inside(skill_dir, file_path)
    if not target.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    size = target.stat().st_size
    if size > config.max_file_bytes:
        raise ValueError(f"File too large: {size} bytes")

    try:
        content = target.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise ValueError("File is not UTF-8 text")

    return FileContent(content=content, path=str(target), size=size)
