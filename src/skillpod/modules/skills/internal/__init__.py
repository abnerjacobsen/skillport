"""Internal implementations for the skills module."""

from .manager import (
    resolve_source,
    detect_skills,
    add_builtin,
    add_local,
    remove_skill,
    SkillInfo,
)
from .validation import validate_skill_record
from .github import parse_github_url, fetch_github_source, ParsedGitHubURL
from .origin import record_origin, remove_origin as remove_origin_record

__all__ = [
    "resolve_source",
    "detect_skills",
    "add_builtin",
    "add_local",
    "remove_skill",
    "SkillInfo",
    "validate_skill_record",
    "parse_github_url",
    "fetch_github_source",
    "ParsedGitHubURL",
    "record_origin",
    "remove_origin_record",
]
