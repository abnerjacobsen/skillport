"""Typer-based CLI entry point.

SkillPod CLI provides commands to manage AI agent skills:
- search: Find skills by query
- show: Display skill details
- add: Install skills from various sources
- list: Show installed skills
- remove: Uninstall skills
- lint: Validate skill definitions
- serve: Start MCP server
"""

from typing import Optional

import typer

from .commands.search import search
from .commands.show import show
from .commands.add import add
from .commands.remove import remove
from .commands.list import list_cmd
from .commands.lint import lint
from .commands.serve import serve
from .theme import VERSION, console


def version_callback(value: bool):
    """Print version and exit."""
    if value:
        console.print(f"skillpod [info]{VERSION}[/info]")
        raise typer.Exit()


app = typer.Typer(
    name="skillpod",
    help="[bold]SkillPod[/bold] - Manage AI agent skills\n\n"
         "A CLI and MCP server for organizing, searching, and serving skills to AI agents.",
    rich_markup_mode="rich",
    no_args_is_help=False,
    add_completion=True,
    pretty_exceptions_show_locals=False,
)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
):
    """SkillPod - Manage AI agent skills."""
    # If no command given, run serve (legacy behavior)
    if ctx.invoked_subcommand is None:
        serve()


# Register commands with enhanced help
app.command(
    "search",
    help="Search for skills matching a query.\n\n"
         "[bold]Examples:[/bold]\n\n"
         "  skillpod search 'PDF extraction'\n\n"
         "  skillpod search code --limit 5\n\n"
         "  skillpod search test --json",
)(search)

app.command(
    "show",
    help="Show skill details and instructions.\n\n"
         "[bold]Examples:[/bold]\n\n"
         "  skillpod show hello-world\n\n"
         "  skillpod show team/code-review\n\n"
         "  skillpod show pdf --json",
)(show)

app.command(
    "add",
    help="Add skills from various sources.\n\n"
         "[bold]Sources:[/bold]\n\n"
         "  [dim]Built-in:[/dim]  hello-world, template\n\n"
         "  [dim]Local:[/dim]     ./my-skill/, ./collection/\n\n"
         "  [dim]GitHub:[/dim]    https://github.com/user/repo\n\n"
         "[bold]Examples:[/bold]\n\n"
         "  skillpod add hello-world\n\n"
         "  skillpod add ./my-skills/ --namespace team\n\n"
         "  skillpod add https://github.com/user/repo --yes",
)(add)

app.command(
    "list",
    help="List installed skills.\n\n"
         "[bold]Examples:[/bold]\n\n"
         "  skillpod list\n\n"
         "  skillpod list --limit 20\n\n"
         "  skillpod list --json",
)(list_cmd)

app.command(
    "remove",
    help="Remove an installed skill.\n\n"
         "[bold]Examples:[/bold]\n\n"
         "  skillpod remove hello-world\n\n"
         "  skillpod remove team/skill --force",
)(remove)

app.command(
    "lint",
    help="Validate skill definitions.\n\n"
         "[bold]Examples:[/bold]\n\n"
         "  skillpod lint\n\n"
         "  skillpod lint hello-world",
)(lint)

app.command(
    "serve",
    help="Start the MCP server.\n\n"
         "[bold]Examples:[/bold]\n\n"
         "  skillpod serve\n\n"
         "  skillpod serve --reindex",
)(serve)


def run():
    """Entry point for CLI."""
    app()
