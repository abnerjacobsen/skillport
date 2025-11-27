import typer
from rich.console import Console
from rich.syntax import Syntax

from skillpod.modules.skills import load_skill
from skillpod.shared.config import Config

console = Console()


def show(
    skill_id: str = typer.Argument(
        ..., help="Skill id (e.g., hello-world or ns/skill)"
    ),
    json_output: bool = typer.Option(False, "--json", help="Output JSON"),
):
    config = Config()
    detail = load_skill(skill_id, config=config)

    if json_output:
        console.print_json(data=detail.model_dump())
        return

    console.print(f"[bold cyan]{detail.id}[/bold cyan] - {detail.name}")
    console.print(detail.description)
    console.print(f"[dim]{detail.path}[/dim]")
    console.print("\n[bold]Instructions[/bold]")
    console.print(Syntax(detail.instructions, "markdown", theme="ansi_light"))
