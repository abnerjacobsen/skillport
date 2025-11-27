import typer
from rich.console import Console
from rich.table import Table

from skillpod.modules.skills import list_skills, ListResult
from skillpod.shared.config import Config

console = Console()


def list_cmd(
    json_output: bool = typer.Option(False, "--json", help="Output JSON"),
    limit: int = typer.Option(100, "--limit", "-n", help="Max items"),
):
    config = Config()
    result: ListResult = list_skills(config=config, limit=limit)

    if json_output:
        console.print_json(data=result.model_dump())
        return

    table = Table(title=f"Skills ({result.total})")
    table.add_column("ID", style="cyan")
    table.add_column("Category")
    table.add_column("Description")
    for skill in result.skills:
        table.add_row(skill.id, skill.category or "-", skill.description[:80])
    console.print(table)
