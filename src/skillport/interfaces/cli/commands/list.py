"""List installed skills command."""

import typer
from rich.table import Table

from skillsouko.modules.skills import list_skills, ListResult
from skillsouko.shared.config import Config
from ..theme import console, empty_skills_panel


def list_cmd(
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON (for scripting/AI agents)",
    ),
    limit: int = typer.Option(
        100,
        "--limit",
        "-n",
        help="Maximum number of skills to display",
        min=1,
        max=1000,
    ),
):
    """List all installed skills."""
    config = Config()
    result: ListResult = list_skills(config=config, limit=limit)

    if json_output:
        console.print_json(data=result.model_dump())
        return

    # Empty state with guidance
    if result.total == 0:
        console.print(empty_skills_panel())
        return

    # Compact table: one skill per line, responsive to terminal width
    table = Table(
        title=f"Skills ({result.total})",
        show_header=True,
        header_style="bold",
        box=None,
        padding=(0, 1),
        expand=True,
    )
    # ID gets ~40% of width, description gets ~60%
    table.add_column("ID", style="cyan", no_wrap=True, ratio=2)
    table.add_column("Description", no_wrap=True, overflow="ellipsis", ratio=3)

    for skill in result.skills:
        # Clean description (remove newlines)
        desc = skill.description.replace("\n", " ").strip()
        table.add_row(skill.id, desc)

    console.print(table)

    # Show truncation notice if applicable
    if result.total > limit:
        console.print(f"[dim]Showing {limit} of {result.total} skills. Use --limit to show more.[/dim]")
