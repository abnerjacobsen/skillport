from typing import Dict, Any
from ..db import SkillDB
from ..utils import is_skill_enabled

class LoadingTools:
    """Tool implementations for loading skills."""

    def __init__(self, db: SkillDB):
        self.db = db
        self.settings = getattr(db, "settings", None)

    def load_skill(self, skill_name: str) -> Dict[str, Any]:
        """Get instructions for a skill. Call this before using any skill.

        The skill_name can come from:
        - User's request ("use X skill")
        - Pre-loaded skills list
        - search_skills results

        Args:
            skill_name: Exact skill name

        Returns:
            name: Skill name
            instructions: Step-by-step instructions to follow
        """
        # 1. Check if exists in DB
        record = self.db.get_skill(skill_name)
        if not record:
            raise ValueError(f"Skill not found: {skill_name}")
        
        # 2. Check if enabled
        if not is_skill_enabled(skill_name, record.get("category"), settings_obj=self.settings):
            raise ValueError(f"Skill is disabled: {skill_name}")
        
        # 3. Return instructions
        return {
            "name": skill_name,
            "instructions": record["instructions"]
        }
