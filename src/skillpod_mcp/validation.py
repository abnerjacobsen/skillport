"""Skill validation and UI elements for SkillPod.

This module provides:
- Validation logic for Agent Skills spec compliance
- ASCII art banners and trophy
- Startup status reporting
"""

import os
import re
import sys
from typing import Dict, List, Any

from .db import SkillDB

# --- Validation Constants (Agent Skills Spec) ---
SKILL_LINE_THRESHOLD = 200
NAME_MAX_LENGTH = 64
NAME_PATTERN = re.compile(r"^[a-z0-9-]+$")
NAME_RESERVED_WORDS = {"anthropic", "claude"}
DESCRIPTION_MAX_LENGTH = 1024
XML_TAG_PATTERN = re.compile(r"<[^>]+>")

# --- ASCII Art ---
SKILLPOD_BANNER = r"""
░██████╗██╗░░██╗██╗██╗░░░░░██╗░░░░░██████╗░░█████╗░██████╗░
██╔════╝██║░██╔╝██║██║░░░░░██║░░░░░██╔══██╗██╔══██╗██╔══██╗
╚█████╗░█████═╝░██║██║░░░░░██║░░░░░██████╔╝██║░░██║██║░░██║
░╚═══██╗██╔═██╗░██║██║░░░░░██║░░░░░██╔═══╝░██║░░██║██║░░██║
██████╔╝██║░╚██╗██║███████╗███████╗██║░░░░░╚█████╔╝██████╔╝
╚═════╝░╚═╝░░╚═╝╚═╝╚══════╝╚══════╝╚═╝░░░░░░╚════╝░╚═════╝░
"""

TROPHY_ART = """
       ___________
      '._==_==_=_.'
      .-\\:      /-.
     | (|:.     |) |
      '-|:.     |-'
        \\::.    /
         '::. .'
           ) (
         _.' '._
        '-------'
"""


def validate_skill(skill: Dict[str, Any]) -> List[str]:
    """Validate a skill against Agent Skills spec. Returns list of issues."""
    issues: List[str] = []
    name = skill.get("name", "")
    description = skill.get("description", "")
    lines = skill.get("lines", 0)
    path = skill.get("path", "")

    # Extract directory name from path
    dir_name = os.path.basename(path) if path else ""

    # Required fields check
    if not name:
        issues.append("frontmatter.name: missing (required)")
    if not description:
        issues.append("frontmatter.description: missing (required)")

    # Name/directory match check (Agent Skills spec requirement)
    if name and dir_name and name != dir_name:
        issues.append(f"frontmatter.name: '{name}' doesn't match directory '{dir_name}'")

    # Lines check
    if lines > SKILL_LINE_THRESHOLD:
        issues.append(f"SKILL.md: {lines} lines (recommended: ≤{SKILL_LINE_THRESHOLD})")

    # Name format checks
    if name:
        if len(name) > NAME_MAX_LENGTH:
            issues.append(f"frontmatter.name: {len(name)} chars (max: {NAME_MAX_LENGTH})")
        if not NAME_PATTERN.match(name):
            issues.append("frontmatter.name: invalid chars (use a-z, 0-9, -)")
        for reserved in NAME_RESERVED_WORDS:
            if reserved in name.lower():
                issues.append(f"frontmatter.name: contains reserved word '{reserved}'")
                break

    # Description format checks
    if description:
        if len(description) > DESCRIPTION_MAX_LENGTH:
            issues.append(f"frontmatter.description: {len(description)} chars (max: {DESCRIPTION_MAX_LENGTH})")
        if XML_TAG_PATTERN.search(description):
            issues.append("frontmatter.description: contains <xml> tags")

    return issues


def report_skill_status(db: SkillDB) -> None:
    """Report skill status at startup with validation.

    Groups skills by issues, shows problem skills first with details.
    Displays ASCII art celebration when all skills pass.
    """
    try:
        all_skills = db.list_all_skills(limit=1000)
        if not all_skills:
            print("[INFO] No skills found.", file=sys.stderr)
            return

        skill_count = len(all_skills)

        # Validate all skills
        skills_with_issues: List[tuple] = []  # (skill, issues)
        ok_skills: List[Dict[str, Any]] = []

        for skill in all_skills:
            issues = validate_skill(skill)
            if issues:
                skills_with_issues.append((skill, issues))
            else:
                ok_skills.append(skill)

        # Sort by number of issues (most problematic first)
        skills_with_issues.sort(key=lambda x: len(x[1]), reverse=True)

        print(f"\n[INFO] {skill_count} skill(s) indexed", file=sys.stderr)

        if skills_with_issues:
            issue_count = len(skills_with_issues)
            max_show = 5
            print(f"\n⚠ {issue_count} skill(s) need attention:", file=sys.stderr)

            for i, (skill, issues) in enumerate(skills_with_issues):
                if i >= max_show:
                    remaining = issue_count - max_show
                    print(f"  ... and {remaining} more with issues", file=sys.stderr)
                    break
                name = skill.get("name", "unknown")
                print(f"  {name}:", file=sys.stderr)
                for issue in issues:
                    print(f"    · {issue}", file=sys.stderr)

            ok_count = len(ok_skills)
            if ok_count > 0:
                print(f"\n✓ {ok_count} skill(s) OK", file=sys.stderr)

            print("\nRun 'skillpod-mcp --lint' for full report.", file=sys.stderr)
        else:
            # All skills pass - celebration!
            print(f"""{TROPHY_ART}
  ✓ All {skill_count} skill(s) pass validation!
""", file=sys.stderr)

    except Exception as e:
        print(f"[WARN] Failed to report skill status: {e}", file=sys.stderr)
