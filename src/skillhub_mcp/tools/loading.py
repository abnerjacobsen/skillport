from typing import Dict, Any
from ..db import db
from ..utils import is_skill_enabled

def load_skill(skill_name: str) -> Dict[str, Any]:
    """
    Load instructions for a specific skill.
    """
    # 1. Check if exists in DB
    record = db.get_skill(skill_name)
    if not record:
        raise ValueError(f"Skill not found: {skill_name}")
    
    # 2. Check if enabled
    if not is_skill_enabled(skill_name, record.get("category")):
        raise ValueError(f"Skill is disabled: {skill_name}")
    
    # 3. Return instructions
    return {
        "name": skill_name,
        "instructions": record["instructions"]
    }
