import typer

from skillpod.interfaces.mcp.server import run_server
from skillpod.shared.config import Config


def serve(
    reindex: bool = typer.Option(False, "--reindex", help="Force reindex before start"),
    skip_auto_reindex: bool = typer.Option(
        False, "--skip-auto-reindex", help="Skip automatic reindex decision"
    ),
):
    config = Config()
    run_server(
        config=config, force_reindex=reindex, skip_auto_reindex=skip_auto_reindex
    )
