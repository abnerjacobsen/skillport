import typer
from rich.console import Console

from skillpod.modules.skills import add_skill
from skillpod.shared.config import Config

console = Console()


def add(
    source: str = typer.Argument(..., help="Built-in name, local path, or GitHub URL"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing"),
    keep_structure: bool = typer.Option(
        False,
        "--keep-structure",
        help="Preserve directory structure when multiple skills",
    ),
    namespace: str | None = typer.Option(
        None, "--namespace", "-n", help="Namespace to use when keeping structure"
    ),
    name: str | None = typer.Option(
        None, "--name", help="Rename single skill to this name"
    ),
):
    config = Config()
    result = add_skill(
        source,
        config=config,
        force=force,
        keep_structure=keep_structure,
        namespace=namespace,
        name=name,
    )
    if result.success:
        console.print(f"[green]✓ {result.message}[/green]")
    else:
        console.print(f"[red]✗ {result.message}[/red]")
        raise typer.Exit(code=1)
