"""Skill management facade for CLI-facing operations."""

from .types import SourceType, SkillInfo, AddResult
from .add import (
    BUILTIN_SKILLS,
    resolve_source,
    detect_skills,
    add_builtin,
    add_local,
)
from .remove import remove_skill
from .github import parse_github_url, fetch_github_source
from .origin import record_origin, remove_origin

__all__ = [
    "SourceType",
    "SkillInfo",
    "AddResult",
    "BUILTIN_SKILLS",
    "resolve_source",
    "detect_skills",
    "add_builtin",
    "add_local",
    "remove_skill",
    "parse_github_url",
    "fetch_github_source",
    "record_origin",
    "remove_origin",
]
