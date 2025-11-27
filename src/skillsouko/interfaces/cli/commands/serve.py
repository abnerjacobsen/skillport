"""Start MCP server command."""


import typer

from skillsouko.interfaces.mcp.server import run_server
from skillsouko.shared.config import Config
from ..theme import stderr_console, VERSION


def serve(
    reindex: bool = typer.Option(
        False,
        "--reindex",
        help="Force reindex before starting server",
    ),
    skip_auto_reindex: bool = typer.Option(
        False,
        "--skip-auto-reindex",
        help="Skip automatic reindex check",
    ),
):
    """Start the MCP server for AI agent integration."""
    config = Config()

    # Log startup info to stderr (stdout is reserved for MCP JSON-RPC)
    stderr_console.print(f"[dim]SkillSouko MCP Server v{VERSION}[/dim]", highlight=False)
    stderr_console.print(f"[dim]Skills: {config.skills_dir}[/dim]", highlight=False)
    stderr_console.print(f"[dim]Index:  {config.db_path}[/dim]", highlight=False)
    stderr_console.print(f"[dim]Provider: {config.embedding_provider}[/dim]", highlight=False)

    if reindex:
        stderr_console.print("[dim]Mode: Force reindex[/dim]", highlight=False)
    elif skip_auto_reindex:
        stderr_console.print("[dim]Mode: Skip auto-reindex[/dim]", highlight=False)

    stderr_console.print("[dim]─" * 40 + "[/dim]", highlight=False)

    run_server(
        config=config, force_reindex=reindex, skip_auto_reindex=skip_auto_reindex
    )
