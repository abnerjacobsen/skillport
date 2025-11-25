"""
Setup detection and readiness checking for skills.

Based on EXECUTION_ENV.md v2.2:
- Auto-detect setup commands from dependency files
- Ready check for skills that require setup
- Runtime resolution (prefer skill-local environments)
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Internal representation: list of commands for sequential execution
# Note: --no-project is required to avoid uv discovering parent pyproject.toml
# Note: -p .venv specifies the target Python for pip install
SETUP_COMMANDS: Dict[str, List[List[str]]] = {
    # Python - uv
    "uv.lock": [["uv", "sync"]],
    "pyproject.toml": [["uv", "sync"]],
    "requirements.txt": [
        ["uv", "venv", "--no-project", ".venv"],
        ["uv", "pip", "install", "-p", ".venv", "-r", "requirements.txt"],
    ],
    # Node.js
    "pnpm-lock.yaml": [["pnpm", "install"]],
    "yarn.lock": [["yarn", "install"]],
    "package-lock.json": [["npm", "ci"]],
    "package.json": [["npm", "install"]],
    # Unsupported (hint only, requires manual install of tool)
    "poetry.lock": [["poetry", "install"]],
    "Pipfile.lock": [["pipenv", "install"]],
    "bun.lockb": [["bun", "install"]],
}

# Files that indicate unsupported package managers (check first for accurate hints)
UNSUPPORTED_FILES = ["poetry.lock", "Pipfile.lock", "bun.lockb"]


def detect_setup_command(skill_dir: Path) -> Tuple[Optional[List[List[str]]], Optional[str]]:
    """
    Detect the appropriate setup command by scanning the skill directory for dependency files.

    Returns:
        (command_list, detected_from_file)
        - command_list: List of commands to execute sequentially, or None if no setup needed
        - detected_from_file: The file that triggered the detection, or None

    Priority:
        1. Unsupported tools first (poetry.lock, Pipfile.lock, bun.lockb) - for accurate hints
        2. Python - uv preferred (uv.lock > pyproject.toml > requirements.txt)
        3. Node.js - lockfile determines tool (pnpm > yarn > npm)
    """
    # Unsupported tools - check FIRST to give accurate hints
    if (skill_dir / "poetry.lock").exists():
        return (SETUP_COMMANDS["poetry.lock"], "poetry.lock")
    if (skill_dir / "Pipfile.lock").exists():
        return (SETUP_COMMANDS["Pipfile.lock"], "Pipfile.lock")
    if (skill_dir / "bun.lockb").exists():
        return (SETUP_COMMANDS["bun.lockb"], "bun.lockb")

    # Python - uv preferred
    if (skill_dir / "uv.lock").exists():
        return (SETUP_COMMANDS["uv.lock"], "uv.lock")
    if (skill_dir / "pyproject.toml").exists():
        return (SETUP_COMMANDS["pyproject.toml"], "pyproject.toml")
    if (skill_dir / "requirements.txt").exists():
        return (SETUP_COMMANDS["requirements.txt"], "requirements.txt")

    # Node.js - lockfile determines tool
    if (skill_dir / "pnpm-lock.yaml").exists():
        return (SETUP_COMMANDS["pnpm-lock.yaml"], "pnpm-lock.yaml")
    if (skill_dir / "yarn.lock").exists():
        return (SETUP_COMMANDS["yarn.lock"], "yarn.lock")
    if (skill_dir / "package-lock.json").exists():
        return (SETUP_COMMANDS["package-lock.json"], "package-lock.json")
    if (skill_dir / "package.json").exists():
        return (SETUP_COMMANDS["package.json"], "package.json")

    return (None, None)


def format_setup_command(commands: List[List[str]]) -> str:
    """
    Format command list for display.

    Example:
        [["uv", "venv"], ["uv", "pip", "install", "-r", "requirements.txt"]]
        -> "uv venv && uv pip install -r requirements.txt"
    """
    return " && ".join(" ".join(cmd) for cmd in commands)


def get_ready_check_path(runtime: str) -> Optional[str]:
    """
    Get the path to check for readiness based on runtime.

    Returns:
        Relative path to check, or None if always ready.

    Per EXECUTION_ENV.md v2.2:
        - python + requires_setup: .venv/bin/python
        - node + requires_setup: node_modules
        - none or requires_setup=false: always ready
    """
    if runtime == "python":
        return ".venv/bin/python"
    elif runtime == "node":
        return "node_modules"
    return None


def check_skill_ready(skill_dir: Path, runtime: str, requires_setup: bool) -> Dict[str, Any]:
    """
    Check if a skill is ready for execution.

    Returns:
        {
            "ready": bool,
            "missing": str | None,  # Path that's missing if not ready
            "setup": {              # Only present if not ready
                "commands": List[List[str]],
                "detected_from": str,
                "display_command": str,
                "full_command": str
            } | None
        }
    """
    # Skills without setup requirement are always ready
    if not requires_setup:
        return {"ready": True, "missing": None}

    # Check runtime-specific path
    check_path = get_ready_check_path(runtime)
    if check_path is None:
        return {"ready": True, "missing": None}

    target = skill_dir / check_path
    if target.exists():
        return {"ready": True, "missing": None}

    # Not ready - detect setup command
    commands, detected_from = detect_setup_command(skill_dir)
    setup_info = None
    if commands:
        display_cmd = format_setup_command(commands)
        setup_info = {
            "commands": commands,
            "detected_from": detected_from,
            "display_command": display_cmd,
            "full_command": f"cd {skill_dir} && {display_cmd}",
        }

    return {
        "ready": False,
        "missing": check_path,
        "setup": setup_info,
    }


def resolve_python_executable(skill_dir: Path) -> str:
    """
    Resolve the Python executable for a skill.

    Priority:
        1. skill_dir/.venv/bin/python (if exists)
        2. System PATH python3
        3. System PATH python

    Returns:
        The executable path or name to use.
    """
    venv_python = skill_dir / ".venv" / "bin" / "python"
    if venv_python.exists():
        return str(venv_python)
    return "python3"


def resolve_node_executable(skill_dir: Path) -> str:
    """
    Resolve the Node.js executable for a skill.

    Node.js is always from system PATH (not installed in node_modules).
    """
    return "node"


def resolve_uv_environment(skill_dir: Path) -> Dict[str, str]:
    """
    Get environment variables for uv execution.

    Sets UV_PROJECT_ENVIRONMENT to skill-local .venv.
    """
    venv_path = skill_dir / ".venv"
    return {"UV_PROJECT_ENVIRONMENT": str(venv_path)}


def get_skill_status(skill_dir: Path, runtime: str, requires_setup: bool) -> Dict[str, Any]:
    """
    Get the status of a skill for startup reporting.

    Returns:
        {
            "ready": bool,
            "status": "READY" | "NOT READY",
            "reason": str,  # "no setup required" | "prompt-only" | "setup complete" | specific missing info
            "setup_hint": str | None  # Full command to run if not ready
        }
    """
    if not requires_setup:
        if runtime == "none":
            return {
                "ready": True,
                "status": "READY",
                "reason": "prompt-only",
                "setup_hint": None,
            }
        return {
            "ready": True,
            "status": "READY",
            "reason": "no setup required",
            "setup_hint": None,
        }

    ready_result = check_skill_ready(skill_dir, runtime, requires_setup)
    if ready_result["ready"]:
        return {
            "ready": True,
            "status": "READY",
            "reason": "setup complete",
            "setup_hint": None,
        }

    # Not ready
    setup_info = ready_result.get("setup")
    setup_hint = None
    if setup_info:
        setup_hint = setup_info.get("full_command")

    return {
        "ready": False,
        "status": "NOT READY",
        "reason": f"Missing: {ready_result['missing']}",
        "setup_hint": setup_hint,
    }


def resolve_runtime_executable(skill_dir: Path, command: str, runtime: str) -> Tuple[str, Dict[str, str]]:
    """
    Resolve the actual executable and environment for a command.

    Args:
        skill_dir: The skill's directory
        command: The command name (python, python3, node, uv, etc.)
        runtime: The skill's runtime type

    Returns:
        (executable_path, environment_vars)
    """
    env_vars: Dict[str, str] = {}

    if command in ("python", "python3"):
        executable = resolve_python_executable(skill_dir)
        return (executable, env_vars)

    if command == "node":
        return (resolve_node_executable(skill_dir), env_vars)

    if command == "uv":
        env_vars = resolve_uv_environment(skill_dir)
        return ("uv", env_vars)

    # Other commands: use as-is from PATH
    return (command, env_vars)
