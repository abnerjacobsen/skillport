"""Transitional entry point dispatching to CLI or MCP server."""

import sys

from skillsouko.interfaces.cli.app import app
from skillsouko.interfaces.mcp.server import run_server
from skillsouko.shared.config import Config


def main():
    args = sys.argv[1:]
    # Legacy: no args → run MCP server (backward compat)
    # Note: `skillsouko --reindex` is NOT supported; use `skillsouko serve --reindex`
    if not args:
        config = Config()
        run_server(config=config)
    else:
        app()


if __name__ == "__main__":
    main()
