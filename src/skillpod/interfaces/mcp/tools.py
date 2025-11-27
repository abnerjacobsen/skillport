from typing import Any, Dict

from fastmcp import FastMCP

from skillpod.modules.skills import load_skill, read_skill_file, search_skills
from skillpod.shared.config import Config


def register_tools(mcp: FastMCP, config: Config):
    """Register MCP tools."""

    @mcp.tool(name="search_skills")
    def search_skills_tool(query: str) -> Dict[str, Any]:
        """Find skills relevant to a task description.

        Use this to discover skills. If you already have a skill_id, skip to load_skill.
        If too many results, refine your query with more specific terms instead of loading more.

        Args:
            query: Natural-language task (e.g., "extract PDF text"). Use "" or "*" to list all.

        Returns:
            skills: Top matches as {id, description, score}. Higher score = better match.
            total: Total matching skills. If high, use a more specific query.
        """
        result = search_skills(query, limit=config.search_limit, config=config)
        skills_list = []
        for s in result.skills:
            item: Dict[str, Any] = {
                "id": s.id,
                "description": s.description,
                "score": s.score,
            }
            # Only include name if it differs from id
            if s.name != s.id:
                item["name"] = s.name
            skills_list.append(item)
        return {"skills": skills_list, "total": result.total}

    @mcp.tool(name="load_skill")
    def load_skill_tool(skill_id: str) -> Dict[str, Any]:
        """Load a skill's instructions and absolute filesystem path.

        Call this after selecting an id from search_skills. The returned `path` is
        required for executing scripts (e.g., `python {path}/script.py`).

        Args:
            skill_id: Skill identifier (e.g., "hello-world" or "namespace/skill").

        Returns:
            id, name, description, instructions, path (absolute directory).
        """
        detail = load_skill(skill_id, config=config)
        return {
            "id": detail.id,
            "name": detail.name,
            "description": detail.description,
            "instructions": detail.instructions,
            "path": detail.path,
        }

    @mcp.tool(name="read_skill_file")
    def read_skill_file_tool(skill_id: str, file_path: str) -> Dict[str, Any]:
        """Read a text file inside a skill (templates, configs).

        Use when instructions reference a file. For scripts, execute via path instead of reading.
        Rejects "../" traversal. UTF-8 only, max ~64KB.

        Args:
            skill_id: Skill identifier from load_skill.
            file_path: Relative path (e.g., "templates/config.json").

        Returns:
            content (UTF-8 text), path (absolute), size (bytes).
        """
        content = read_skill_file(skill_id, file_path, config=config)
        return {"content": content.content, "path": content.path, "size": content.size}


__all__ = ["register_tools"]
