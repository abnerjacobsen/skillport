from typing import Dict, Any
from ..db import SkillDB
from ..utils import is_skill_enabled


class LoadingTools:
    """Tool implementations for loading skills."""

    def __init__(self, db: SkillDB):
        self.db = db
        self.settings = getattr(db, "settings", None)

    def load_skill(self, skill_id: str | None = None, skill_name: str | None = None) -> Dict[str, Any]:
        """Load a skill's full instructions and directory path.

        Args:
            skill_id: Skill id (preferred, supports namespaces).
            skill_name: Legacy alias for skill id.

        Returns:
            id: Skill identifier (path-like)
            name: Leaf skill name
            instructions: Step-by-step guidance to follow
            path: Skill directory. Execute scripts in your terminal: `python {path}/script.py`
        """
        identifier = skill_id or skill_name
        if not identifier:
            raise ValueError("skill_id is required")

        # 1. Check if exists in DB
        try:
            record = self.db.get_skill(identifier)
        except ValueError as e:
            # Propagate with a friendlier hint
            raise ValueError(f"{e}. Use full skill_id (e.g., group/skill) or search_skills to disambiguate.") from e

        if not record:
            raise ValueError(f"Skill not found: {identifier}. Run search_skills(\"\") to list available ids.")

        # 2. Check if enabled
        skill_identifier = record.get("id", identifier)
        if not is_skill_enabled(skill_identifier, record.get("category"), settings_obj=self.settings):
            raise ValueError(f"Skill is disabled: {skill_identifier}")

        # 3. Return instructions with path
        return {
            "id": skill_identifier,
            "name": record.get("name", skill_identifier),
            "instructions": record["instructions"],
            "path": record.get("path", ""),
        }
