"""CLI-only modes for SkillHub (--lint, --list).

This module handles CLI flags and standalone commands that don't start the server.
"""

import os
import sys
from typing import Dict, List, Any

from .db import SkillDB
from .validation import (
    TROPHY_ART,
    validate_skill,
)

# CLI flags
KNOWN_FLAGS = {"--reindex", "--skip-auto-reindex", "--lint", "--list"}


def parse_flags() -> Dict[str, Any]:
    """Parse CLI flags and return a dict of flag states."""
    argv = sys.argv[1:]

    # Check for --lint [skill-name]
    lint_mode = "--lint" in argv
    lint_skill = None
    if lint_mode:
        lint_idx = argv.index("--lint")
        # Check if there's a skill name after --lint
        if lint_idx + 1 < len(argv) and not argv[lint_idx + 1].startswith("--"):
            lint_skill = argv[lint_idx + 1]
            argv = argv[:lint_idx] + argv[lint_idx + 2:]  # Remove --lint and skill name
        else:
            argv = argv[:lint_idx] + argv[lint_idx + 1:]  # Remove just --lint

    list_mode = "--list" in argv

    flags = {
        "force_reindex": "--reindex" in argv,
        "skip_auto": ("--skip-auto-reindex" in argv) or (os.getenv("SKILLHUB_SKIP_AUTO_REINDEX") == "1"),
        "lint": lint_mode,
        "lint_skill": lint_skill,
        "list": list_mode,
    }
    # strip known flags so FastMCP doesn't see them
    sys.argv = [sys.argv[0]] + [a for a in argv if a not in KNOWN_FLAGS]
    return flags


def _ensure_index(db: SkillDB) -> None:
    """Ensure index is up to date before CLI operations."""
    reindex_decision = db.should_reindex(force=False, skip_auto=False)
    if reindex_decision["need"]:
        db.initialize_index()
        db.persist_state(reindex_decision["state"])


def run_lint(db: SkillDB, skill_name: str | None = None) -> int:
    """Run detailed lint validation. Returns exit code (0=pass, 1=fail)."""
    all_skills = db.list_all_skills(limit=1000)
    if not all_skills:
        print("No skills found.")
        return 1

    # Filter to specific skill if requested
    if skill_name:
        all_skills = [s for s in all_skills if s.get("name") == skill_name]
        if not all_skills:
            print(f"Skill '{skill_name}' not found.")
            return 1

    print(f"{'─' * 50}")
    print(f" Validating {len(all_skills)} skill(s)")
    print(f"{'─' * 50}")

    # Collect only skills with issues
    skills_with_issues: List[tuple] = []
    for skill in all_skills:
        issues = validate_skill(skill)
        if issues:
            skills_with_issues.append((skill, issues))

    # Sort by number of issues (most problematic first)
    skills_with_issues.sort(key=lambda x: len(x[1]), reverse=True)

    ok_count = len(all_skills) - len(skills_with_issues)

    if not skills_with_issues:
        # All pass - trophy!
        print(TROPHY_ART)
        print(f"  ✓ All {len(all_skills)} skill(s) pass validation!")
        print(f"{'─' * 50}\n")
        return 0

    # Show issues only
    print(f"\n⚠ {len(skills_with_issues)} skill(s) with issues:\n")

    for skill, issues in skills_with_issues:
        name = skill.get("name", "unknown")
        print(f"  {name}")
        for issue in issues:
            print(f"    · {issue}")
        print()

    print(f"{'─' * 50}")
    print(f"  {len(skills_with_issues)} with issues / {ok_count} OK")
    print(f"{'─' * 50}\n")
    return 1


def run_list(db: SkillDB) -> int:
    """List all skills without starting the server. Returns exit code."""
    all_skills = db.list_all_skills(limit=1000)
    if not all_skills:
        print("No skills found.")
        return 1

    # Sort by name
    all_skills.sort(key=lambda s: s.get("name", ""))

    print(f"{'─' * 60}")
    print(f" {len(all_skills)} skill(s)")
    print(f"{'─' * 60}\n")

    for skill in all_skills:
        name = skill.get("name", "unknown")
        description = skill.get("description", "")
        always_apply = skill.get("always_apply", False)
        # Truncate description for display
        desc_display = description[:40] + "..." if len(description) > 40 else description
        marker = "★" if always_apply else " "
        print(f"  {marker} {name:<24} {desc_display}")

    print(f"\n{'─' * 60}\n")
    return 0


def handle_cli_mode() -> bool:
    """Handle CLI-only modes (--lint, --list).

    Returns True if a CLI mode was handled (and program should exit),
    False if normal server startup should proceed.
    """
    argv = sys.argv[1:]

    # --lint mode
    if "--lint" in argv:
        flags = parse_flags()
        db = SkillDB()
        _ensure_index(db)
        exit_code = run_lint(db, flags.get("lint_skill"))
        sys.exit(exit_code)

    # --list mode
    if "--list" in argv:
        parse_flags()  # consume flags
        db = SkillDB()
        _ensure_index(db)
        exit_code = run_list(db)
        sys.exit(exit_code)

    return False
