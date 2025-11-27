from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from skillpod.modules.skills.internal import validate_skill_record
from .types import SkillSummary, ValidationResult


def _coerce_summary(skill: SkillSummary | Mapping[str, Any]) -> SkillSummary:
    """Accept dicts from index results and coerce to SkillSummary.

    list_all() returns plain dicts; lint should still reuse validate_skill.
    Normalizes category per core principles (trim+lowercase).
    """
    if isinstance(skill, SkillSummary):
        return skill
    if not isinstance(skill, Mapping):
        raise TypeError(f"Unsupported skill type for validation: {type(skill)}")
    data = {
        "id": skill.get("id") or skill.get("name"),
        "name": skill.get("name") or skill.get("id") or "",
        "description": skill.get("description") or "",
        "category": (skill.get("category") or "").strip().lower(),
        "score": skill.get("score", 0.0) or 0.0,
    }
    return SkillSummary.model_validate(data)


def validate_skill(skill: SkillSummary | Mapping[str, Any]) -> ValidationResult:
    """Validate a skill summary (SkillSummary or dict from index)."""
    summary = _coerce_summary(skill)
    issues = validate_skill_record(summary.model_dump())
    valid = all(issue.severity != "fatal" for issue in issues)
    return ValidationResult(valid=valid, issues=issues, skill_id=summary.id)
