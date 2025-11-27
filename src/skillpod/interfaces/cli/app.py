"""Typer-based CLI entry point."""

import typer

from .commands.search import search
from .commands.show import show
from .commands.add import add
from .commands.remove import remove
from .commands.list import list_cmd
from .commands.lint import lint
from .commands.serve import serve

app = typer.Typer(help="SkillPod CLI")

app.command("search")(search)
app.command("show")(show)
app.command("add")(add)
app.command("remove")(remove)
app.command("list")(list_cmd)
app.command("lint")(lint)
app.command("serve")(serve)


def run():
    app()
