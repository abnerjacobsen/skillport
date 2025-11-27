import shutil
from pathlib import Path

from .types import AddResult


def _assert_inside(target_dir: Path, skill_path: Path) -> None:
    """Ensure skill_path stays within target_dir to avoid traversal."""
    try:
        if not skill_path.resolve().is_relative_to(target_dir.resolve()):
            raise PermissionError(f"{skill_path} is outside {target_dir}")
    except AttributeError:
        # Python <3.9 fallback
        from os import path as osp

        if osp.commonpath([target_dir.resolve(), skill_path.resolve()]) != str(target_dir.resolve()):
            raise PermissionError(f"{skill_path} is outside {target_dir}")


def remove_skill(skill_id: str, target_dir: Path) -> AddResult:
    """Remove a skill directory by id."""
    skill_path = target_dir / skill_id
    _assert_inside(target_dir, skill_path)

    if not skill_path.exists():
        return AddResult(False, skill_id, f"Skill not found: {skill_id}")
    if not skill_path.is_dir():
        return AddResult(False, skill_id, f"Not a directory: {skill_path}")

    shutil.rmtree(skill_path)
    return AddResult(True, skill_id, f"Removed '{skill_id}'")
