import sys

from fastmcp import FastMCP

from skillsouko.interfaces.mcp.tools import register_tools
from skillsouko.modules.indexing import build_index, should_reindex, list_all
from skillsouko.shared.config import Config

BANNER = r"""
░██████╗██╗░░██╗██╗██╗░░░░░██╗░░░░░██████╗░░█████╗░██████╗░
██╔════╝██║░██╔╝██║██║░░░░░██║░░░░░██╔══██╗██╔══██╗██╔══██╗
╚█████╗░█████═╝░██║██║░░░░░██║░░░░░██████╔╝██║░░██║██║░░██║
░╚═══██╗██╔═██╗░██║██║░░░░░██║░░░░░██╔═══╝░██║░░██║██║░░██║
██████╔╝██║░╚██╗██║███████╗███████╗██║░░░░░╚█████╔╝██████╔╝
╚═════╝░╚═╝░░╚═╝╚═╝╚══════╝╚══════╝╚═╝░░░░░░╚════╝░╚═════╝░
"""


def _build_instructions(config: Config) -> str:
    base = """# SkillSouko: Agent Skills Server

SkillSouko provides **Agent Skills** — reusable expert knowledge that loads on demand.
Skills use progressive disclosure: search first, load only what you need.

## Workflow

1. **Search**: `search_skills("task description")` → Find skills by what you want to do
2. **Load**: `load_skill(skill_id)` → Get instructions + absolute filesystem `path`
3. **Execute**: Follow the instructions, using `path` to run any scripts

## Path-Based Execution (Important!)

When `load_skill` returns a `path`, use it to execute scripts in the **user's project**:

```bash
# Correct: Use the absolute path from load_skill
python /path/to/skill/scripts/process.py ./input.txt --output ./result.txt

# Wrong: Relative paths won't work
python scripts/process.py ./input.txt
```

Output files should go to the user's working directory, not the skill's directory.

## Available Tools

| Tool | Purpose |
|------|---------|
| `search_skills(query)` | Find skills by description. Use "" or "*" to list all. |
| `load_skill(id)` | Get full instructions and path. Call after search. |
| `read_skill_file(id, file)` | Read templates/configs when instructions say to. |

## Tips

- Don't read script files into context — just execute them via path
- Skill instructions may use `{path}` placeholder — replace with actual path from load_skill
- If search returns nothing, try broader terms or list all with ""
"""
    rows = list_all(limit=200, config=config)
    core = [r for r in rows if r.get("always_apply")]
    if core:
        base += "\n## Core Skills (always available)\n\n"
        base += "These skills are pre-loaded and can be used without searching:\n\n"
        for skill in core:
            sid = skill.get("id") or skill.get("name")
            base += f"- **{sid}**: {skill.get('description', '')}\n"
    return base


def run_server(
    *, config: Config, force_reindex: bool = False, skip_auto_reindex: bool = False
):
    print(BANNER, file=sys.stderr)

    decision = should_reindex(config=config)
    if force_reindex:
        print("[INFO] Reindexing (force)", file=sys.stderr)
        build_index(config=config, force=True)
    elif not skip_auto_reindex and decision.need:
        print(f"[INFO] Reindexing (reason={decision.reason})", file=sys.stderr)
        build_index(config=config, force=False)
    else:
        print(f"[INFO] Skipping reindex (reason={decision.reason})", file=sys.stderr)

    instructions = _build_instructions(config)
    mcp = FastMCP("skillsouko", version="0.0.0", instructions=instructions)
    register_tools(mcp, config)
    mcp.run()
