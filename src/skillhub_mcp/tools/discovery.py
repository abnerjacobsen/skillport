from typing import Dict, Any
from ..config import settings
from ..db import SkillDB
from ..utils import is_skill_enabled

class DiscoveryTools:
    """Tool implementations related to discovery/search."""

    def __init__(self, db: SkillDB):
        self.db = db
        self.settings = getattr(db, "settings", settings)

    def search_skills(self, query: str) -> Dict[str, Any]:
        """Find skills by natural language query.

        Use when you don't know which skill exists for a task.
        Skip if you already know the skill name.
        Pass empty string or "*" to list available skills.

        Args:
            query: What you want to do, or "" / "*" to list all

        Returns:
            skills: List of {name, description, score} sorted by relevance
        """
        limit = self.settings.search_limit
        query_stripped = query.strip()

        # Empty or wildcard query -> list all skills
        if not query_stripped or query_stripped == "*":
            candidates = self.db.list_all_skills(limit=limit * 2)
        else:
            candidates = self.db.search(query, limit=limit)

        # Filter by enabled settings
        results = []
        for cand in candidates:
            name = cand["name"]
            category = cand.get("category")

            if is_skill_enabled(name, category, settings_obj=self.settings):
                score = float(cand.get("_score", 0.0))
                results.append(
                    {
                        "name": name,
                        "description": cand["description"],
                        "score": max(0.0, score),
                    }
                )

            if len(results) >= limit:
                break

        return {"skills": results}
