import typer
from rich.console import Console

from skillpod.modules.skills import remove_skill
from skillpod.shared.config import Config

console = Console()


def remove(
    skill_id: str = typer.Argument(..., help="Skill id to remove"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    if not force:
        confirm = typer.confirm(f"Remove '{skill_id}'?", default=False)
        if not confirm:
            raise typer.Exit(code=1)

    config = Config()
    result = remove_skill(skill_id, config=config)
    if result.success:
        console.print(f"[green]{result.message}[/green]")
    else:
        console.print(f"[red]{result.message}[/red]")
        raise typer.Exit(code=1)
