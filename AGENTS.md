# Agent Guidelines & Context

## 1. Core Principles
*   **Single Source of Truth (SSOT)**: `docs/v0.0.0/PLAN.md` is the living document.
*   **Task Management**: All tasks MUST be tracked in `PLAN.md` using Markdown todo lists (`- [ ] Task`).
    *   Update the status (`- [x]`) immediately upon completion.
    *   Add new tasks/discoveries to `PLAN.md` rather than keeping them in conversation memory.
*   **Web Search**: Use web search to find info about libraries (Model Context Protocol, Agent Skills, LanceDB, etc.).

## 2. Project Context
### Architecture
*   **Name**: `skillhub-mcp`
*   **Type**: MCP Server (Model Context Protocol)
*   **Stack**:
    *   **Runtime**: Python 3.10+
    *   **Package Manager**: `uv`
    *   **MCP Lib**: `fastmcp`
    *   **Database**: `lancedb` (Vector + FTS)
    *   **Config**: `pydantic-settings`

### Directory Structure
*   `src/skillhub_mcp/`: Source code
    *   `server.py`: Server initialization
    *   `tools/`: Tool implementations (discovery, loading, execution)
    *   `db.py`: Database & Search logic
    *   `config.py`: Configuration
*   `docs/v0.0.0/`: Documentation & PLAN.md
*   `.agent/skills/`: Local skills storage for testing
*   `verify_server.py`: Verification script (Mock Client)

## 3. Operation & Verification
To act autonomously, always verify changes using these commands:

*   **Install/Sync**: `uv sync`
*   **Run Server (Manual)**:
    ```bash
    SKILLS_DIR=.agent/skills EMBEDDING_PROVIDER=none uv run skillhub-mcp
    ```
*   **Verify Functionality (Critical)**:
    ```bash
    uv run verify_server.py
    ```
    *   Always run this after modifying `server.py`, `db.py`, or `config.py`.

## 4. Debugging & Logging
*   **MCP Constraints**: The server communicates via `stdout`.
    *   **NEVER** print debug info to `stdout`.
    *   **ALWAYS** use `sys.stderr` for logs/prints.
*   **Logs**: If `verify_server.py` fails, check the `stderr` output captured in the tool result.
