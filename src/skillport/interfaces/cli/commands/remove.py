"""Remove skill command."""

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from skillsouko.modules.skills import remove_skill
from skillsouko.modules.indexing import build_index
from skillsouko.shared.config import Config
from ..theme import console, stderr_console, print_error, print_success, is_interactive


def remove(
    skill_id: str = typer.Argument(
        ...,
        help="Skill ID to remove (e.g., hello-world or namespace/skill)",
        show_default=False,
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Skip confirmation prompt",
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Skip confirmation prompt (alias for --force)",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON (for scripting/AI agents)",
    ),
):
    """Remove an installed skill."""
    # --yes is alias for --force
    skip_confirm = force or yes

    if not skip_confirm and is_interactive():
        confirm = typer.confirm(f"Remove '{skill_id}'?", default=False)
        if not confirm:
            if json_output:
                console.print_json(data={
                    "success": False,
                    "message": "Cancelled by user",
                })
            else:
                console.print("[dim]Cancelled[/dim]")
            raise typer.Exit(code=1)

    config = Config()
    result = remove_skill(skill_id, config=config)

    # Auto-reindex if skill was removed
    if result.success:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=stderr_console,
            transient=True,
        ) as progress:
            progress.add_task("Updating index...", total=None)
            build_index(config=config, force=False)

    if json_output:
        console.print_json(data={
            "success": result.success,
            "message": result.message,
        })
        if not result.success:
            raise typer.Exit(code=1)
        return

    if result.success:
        print_success(result.message)
    else:
        print_error(
            result.message,
            code="SKILL_NOT_FOUND" if "not found" in result.message.lower() else "REMOVE_FAILED",
            suggestion="Run 'skillsouko list' to see available skills",
        )
        raise typer.Exit(code=1)
