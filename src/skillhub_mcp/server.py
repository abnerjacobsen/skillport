import subprocess
import sys
import os
from pathlib import Path
from typing import Dict, List, Any
from fastmcp import FastMCP
from .db import SkillDB
from .tools.discovery import DiscoveryTools
from .tools.loading import LoadingTools
from .tools.execution import ExecutionTools
from .setup import get_skill_status, detect_setup_command, format_setup_command

# CLI flags
KNOWN_FLAGS = {"--reindex", "--skip-auto-reindex", "--setup-list", "--setup-auto"}


def _parse_flags() -> Dict[str, bool]:
    """Parse CLI flags and return a dict of flag states."""
    argv = sys.argv[1:]
    flags = {
        "force_reindex": "--reindex" in argv,
        "skip_auto": ("--skip-auto-reindex" in argv) or (os.getenv("SKILLHUB_SKIP_AUTO_REINDEX") == "1"),
        "setup_list": "--setup-list" in argv,
        "setup_auto": "--setup-auto" in argv,
    }
    # strip known flags so FastMCP doesn't see them
    sys.argv = [sys.argv[0]] + [a for a in argv if a not in KNOWN_FLAGS]
    return flags

def _get_skill_statuses(db: SkillDB) -> List[Dict[str, Any]]:
    """Get status information for all skills."""
    results = []
    all_skills = db.list_all_skills(limit=1000)
    if not all_skills:
        return results

    for skill in all_skills:
        name = skill.get("name", "unknown")
        skill_path = skill.get("path", "")
        runtime = skill.get("runtime", "none")
        requires_setup = skill.get("requires_setup", False)

        if skill_path:
            skill_dir = Path(skill_path)  # path is skill directory, not SKILL.md
            status = get_skill_status(skill_dir, runtime, requires_setup)
            status["skill_dir"] = skill_dir
        else:
            status = {"ready": True, "status": "READY", "reason": "no path", "setup_hint": None, "skill_dir": None}

        status["name"] = name
        status["runtime"] = runtime
        status["requires_setup"] = requires_setup
        results.append(status)

    return results


def _report_skill_status(db: SkillDB) -> None:
    """Report the status of all skills at startup (EXECUTION_ENV.md v2.2 Section 7)."""
    try:
        statuses = _get_skill_statuses(db)
        if not statuses:
            print("[INFO] No skills found.", file=sys.stderr)
            return

        print("[INFO] Skills status:", file=sys.stderr)

        ready_count = 0
        not_ready_skills = []

        for status in statuses:
            name = status["name"]
            if status["ready"]:
                ready_count += 1
                print(f"  {name} {'.' * max(1, 30 - len(name))} READY ({status['reason']})", file=sys.stderr)
            else:
                not_ready_skills.append(status)
                print(f"  {name} {'.' * max(1, 30 - len(name))} NOT READY", file=sys.stderr)
                print(f"      {status['reason']}", file=sys.stderr)
                if status["setup_hint"]:
                    print(f"      Setup: {status['setup_hint']}", file=sys.stderr)

        total = len(statuses)
        if not_ready_skills:
            print(f"\n[WARN] {len(not_ready_skills)} skill(s) require setup. Run the commands above before using them.", file=sys.stderr)
        print(f"[INFO] {ready_count}/{total} skills ready.", file=sys.stderr)

    except Exception as e:
        print(f"[WARN] Failed to report skill status: {e}", file=sys.stderr)


def _cli_setup_list(db: SkillDB) -> int:
    """CLI: Show skill readiness overview (--setup-list)."""
    statuses = _get_skill_statuses(db)
    if not statuses:
        print("No skills found.")
        return 0

    print("SkillHub - Skill Readiness\n")

    ready_skills = [s for s in statuses if s["ready"]]
    not_ready_skills = [s for s in statuses if not s["ready"]]

    if ready_skills:
        print(f"Ready ({len(ready_skills)}):")
        for s in ready_skills:
            print(f"  ✓ {s['name']} ({s['reason']})")
        print()

    if not_ready_skills:
        print(f"Not Ready ({len(not_ready_skills)}):")
        for s in not_ready_skills:
            print(f"  ✗ {s['name']}")
            print(f"    {s['reason']}")
            if s.get("setup_hint"):
                print(f"    Run: {s['setup_hint']}")
        print()

    print(f"Summary: {len(ready_skills)}/{len(statuses)} skills ready")
    if not_ready_skills:
        print("\nRun 'skillhub-mcp --setup-auto' to set up all skills automatically.")

    return 0


def _cli_setup_auto(db: SkillDB) -> int:
    """CLI: Auto-setup all skills that need it (--setup-auto)."""
    statuses = _get_skill_statuses(db)
    not_ready_skills = [s for s in statuses if not s["ready"] and s.get("skill_dir")]

    if not not_ready_skills:
        print("All skills are ready. Nothing to set up.")
        return 0

    print(f"Setting up {len(not_ready_skills)} skill(s)...\n")

    success_count = 0
    failed_skills = []

    for status in not_ready_skills:
        name = status["name"]
        skill_dir = status["skill_dir"]

        print(f"[{name}] Setting up...")

        # Detect setup command
        commands, detected_from = detect_setup_command(skill_dir)
        if not commands:
            print(f"[{name}] No setup command detected. Skipping.")
            failed_skills.append((name, "No setup command detected"))
            continue

        print(f"[{name}] Detected: {detected_from}")
        print(f"[{name}] Running: {format_setup_command(commands)}")

        # Execute commands sequentially
        # Set UV_PROJECT_ENVIRONMENT to ensure uv uses skill-local .venv
        # Use absolute path to avoid issues with relative paths
        skill_dir_abs = skill_dir.resolve()
        env = os.environ.copy()
        env["UV_PROJECT_ENVIRONMENT"] = str(skill_dir_abs / ".venv")

        all_ok = True
        for cmd in commands:
            try:
                result = subprocess.run(
                    cmd,
                    cwd=skill_dir_abs,
                    capture_output=True,
                    text=True,
                    timeout=300,  # 5 min timeout per command
                    env=env,
                )
                if result.returncode != 0:
                    print(f"[{name}] Command failed: {' '.join(cmd)}")
                    if result.stderr:
                        print(f"[{name}] stderr: {result.stderr[:500]}")
                    all_ok = False
                    break
            except subprocess.TimeoutExpired:
                print(f"[{name}] Command timed out: {' '.join(cmd)}")
                all_ok = False
                break
            except Exception as e:
                print(f"[{name}] Error: {e}")
                all_ok = False
                break

        if all_ok:
            print(f"[{name}] ✓ Setup complete\n")
            success_count += 1
        else:
            failed_skills.append((name, "Setup command failed"))
            print(f"[{name}] ✗ Setup failed\n")

    print(f"\nSummary: {success_count}/{len(not_ready_skills)} skills set up successfully")
    if failed_skills:
        print("Failed:")
        for name, reason in failed_skills:
            print(f"  - {name}: {reason}")
        return 1

    return 0


def create_server() -> FastMCP:
    flags = _parse_flags()

    # Instantiate DB explicitly so lifecycle is tied to the server instance.
    db = SkillDB()

    # Decide on index refresh
    reindex_decision = db.should_reindex(force=flags["force_reindex"], skip_auto=flags["skip_auto"])
    if reindex_decision["need"]:
        print(f"[INFO] Reindexing skills (reason={reindex_decision['reason']})", file=sys.stderr)
        try:
            db.initialize_index()
            db.persist_state(reindex_decision["state"])
        except Exception as e:
            print(f"Warning: Failed to initialize index: {e}", file=sys.stderr)
    else:
        print(f"[INFO] Skipping reindex (reason={reindex_decision['reason']})", file=sys.stderr)

    # Handle CLI commands (exit after running)
    if flags["setup_list"]:
        sys.exit(_cli_setup_list(db))
    if flags["setup_auto"]:
        sys.exit(_cli_setup_auto(db))

    # Report skill status at startup (EXECUTION_ENV.md v2.2)
    _report_skill_status(db)

    # Generate Instructions (concise, minimal)
    core_skills = db.get_core_skills()
    instructions = "SkillHub MCP provides reusable Agent Skills.\n\n"
    if core_skills:
        instructions += "Pre-loaded skills:\n"
        for skill in core_skills:
            instructions += f"- {skill['name']}: {skill['description']}\n"
        instructions += "\n"
    instructions += "Call load_skill(name) to get a skill's instructions.\n"
    instructions += "Call search_skills(query) to find skills."

    # Debug: Print instructions to stderr to verify
    print(f"[DEBUG] Generated Instructions:\n{instructions}", file=sys.stderr)

    # Create MCP Server
    mcp = FastMCP("skillhub-mcp", version="0.0.0", instructions=instructions)

    # Register Tools (methods preserve __name__/__doc__)
    discovery_tools = DiscoveryTools(db)
    loading_tools = LoadingTools(db)
    execution_tools = ExecutionTools(db)

    mcp.tool()(discovery_tools.search_skills)
    mcp.tool()(loading_tools.load_skill)
    mcp.tool()(execution_tools.read_skill_file)
    mcp.tool()(execution_tools.run_skill_command)
    
    return mcp

def main():
    mcp = create_server()
    mcp.run()

if __name__ == "__main__":
    main()
