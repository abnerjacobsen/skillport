from typing import Any, Dict

from fastmcp import FastMCP

from skillpod.modules.skills import load_skill, read_skill_file, search_skills
from skillpod.shared.config import Config


def register_tools(mcp: FastMCP, config: Config):
    """Register MCP tools."""

    @mcp.tool(name="search_skills")
    def search_skills_tool(query: str) -> Dict[str, Any]:
        """Find Agent Skills relevant to a task description.

        When to use:
          - You need a capability and don’t know which skill to load yet.
        When NOT to use:
          - You already have a skill id: go straight to load_skill.
          - You’re browsing files: use read_skill_file after load_skill instead.

        Flow:
          1) Call search_skills with the task text.
          2) Choose a skill `id` from results.
          3) Call load_skill(id) to get executable instructions and path.

        Args:
            query: Natural-language task (e.g., "extract PDF text"). Use "" or "*" to list all enabled skills.

        Returns:
            skills: List of {id, description, score, name?}. name is omitted if same as id. Higher score = better match.
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
        return {"skills": skills_list}

    @mcp.tool(name="load_skill")
    def load_skill_tool(skill_id: str) -> Dict[str, Any]:
        """Load a skill’s instructions and absolute filesystem path.

        Why `path` matters:
          - It is the authoritative location of the skill’s files (scripts, templates, data).
          - Use it when running scripts in your terminal (e.g., `python {path}/script.py`).
          - Do not guess paths or reuse old paths after moving skills—call load_skill again.

        When to use:
          - Right after selecting an id from search_skills.
        When NOT to use:
          - You only need metadata: search_skills is cheaper.
          - You need a specific file’s contents: call read_skill_file after this.

        Args:
            skill_id: Skill identifier (e.g., "hello-world" or "group/skill").

        Returns:
            id, name, description, instructions, path (absolute dir on disk).
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
        """Read a text file inside a loaded skill (templates/configs).

        When to use:
          - You need template/config content to include in context (e.g., a prompt template).
        When NOT to use:
          - Executing code: run the script directly using the `path` from load_skill instead of reading it.
          - Large/binary assets: rejected to protect context (UTF-8 only, max size SKILLPOD_MAX_FILE_BYTES ≈64KB).

        Safety:
          - `file_path` must be relative to the skill root; "../" is rejected to prevent traversal.
          - Returns absolute `path` for transparency; do not execute it here—execute in your terminal if needed.

        Args:
            skill_id: Skill identifier from load_skill.
            file_path: Relative path (e.g., "templates/config.json").

        Returns:
            content: UTF-8 text, path: absolute path, size: byte length.
        """
        content = read_skill_file(skill_id, file_path, config=config)
        return {"content": content.content, "path": content.path, "size": content.size}


__all__ = ["register_tools"]
