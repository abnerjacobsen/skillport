import typer
from rich.console import Console
from rich.table import Table

from skillpod.modules.skills import search_skills, SearchResult
from skillpod.shared.config import Config

console = Console()


def search(
    query: str = typer.Argument(..., help="Search query"),
    limit: int = typer.Option(10, "--limit", "-n", help="Max results"),
    json_output: bool = typer.Option(False, "--json", help="Output JSON"),
):
    config = Config()
    result: SearchResult = search_skills(query, limit=limit, config=config)

    if json_output:
        console.print_json(data=result.model_dump())
        return

    table = Table(title=f"Search: {query}")
    table.add_column("ID", style="cyan")
    table.add_column("Name")
    table.add_column("Description")
    table.add_column("Score", justify="right")

    for skill in result.skills:
        table.add_row(
            skill.id, skill.name, skill.description[:50], f"{skill.score:.2f}"
        )

    console.print(table)
