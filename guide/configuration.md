# Configuration

This guide covers all configuration options for SkillPod.

## Environment Variables

All environment variables are prefixed with `SKILLPOD_`. The prefix is optional for common variables like `SKILLS_DIR`.

### Core Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `SKILLPOD_SKILLS_DIR` | Path to skills directory | `~/.skillpod/skills` |
| `SKILLPOD_DB_PATH` | Path to LanceDB index | `~/.skillpod/indexes/default/` |

### Search

| Variable | Description | Default |
|----------|-------------|---------|
| `SKILLPOD_EMBEDDING_PROVIDER` | Search mode: `none`, `openai`, or `gemini` | `none` |
| `SKILLPOD_SEARCH_LIMIT` | Maximum search results | `10` |
| `SKILLPOD_SEARCH_THRESHOLD` | Minimum score threshold (0-1) | `0.2` |

#### Full-Text Search (Default)

When `SKILLPOD_EMBEDDING_PROVIDER=none` (default), search uses BM25-based full-text search via Tantivy. This is:

- **Fast** — no external API calls
- **Private** — all data stays local
- **Reliable** — no API keys needed

```bash
# No configuration needed — this is the default
SKILLPOD_EMBEDDING_PROVIDER=none
```

#### Vector Search (Optional)

For semantic search across large skill collections, enable vector embeddings:

**OpenAI:**
```bash
export SKILLPOD_EMBEDDING_PROVIDER=openai
export OPENAI_API_KEY=sk-...
export OPENAI_EMBEDDING_MODEL=text-embedding-3-small  # optional
```

**Gemini:**
```bash
export SKILLPOD_EMBEDDING_PROVIDER=gemini
export GEMINI_API_KEY=...
export GEMINI_EMBEDDING_MODEL=gemini-embedding-001  # optional
```

#### Fallback Chain

Search always returns results through a fallback chain:

1. **Vector search** (if enabled) — semantic matching
2. **FTS (BM25)** — keyword matching
3. **Substring match** — last resort

### Execution Limits

| Variable | Description | Default |
|----------|-------------|---------|
| `SKILLPOD_EXEC_TIMEOUT_SECONDS` | Command execution timeout | `60` |
| `SKILLPOD_MAX_FILE_BYTES` | Max file read size | `65536` |

## Client-Based Skill Filtering

Expose different skills to different AI agents by configuring filter environment variables.

| Variable | Description | Default |
|----------|-------------|---------|
| `SKILLPOD_ENABLED_SKILLS` | Comma-separated skill IDs | all |
| `SKILLPOD_ENABLED_CATEGORIES` | Comma-separated categories | all |
| `SKILLPOD_ENABLED_NAMESPACES` | Comma-separated namespaces | all |

### Filter Priority

Filters are evaluated in order of specificity:

1. If `SKILLPOD_ENABLED_SKILLS` is set → only those exact skill IDs
2. Otherwise, if `SKILLPOD_ENABLED_NAMESPACES` is set → only matching prefixes
3. Otherwise, if `SKILLPOD_ENABLED_CATEGORIES` is set → only matching categories
4. If none are set → all skills available

### Examples

**Filter by category:**
```bash
export SKILLPOD_ENABLED_CATEGORIES=development,testing
```

**Filter by specific skills:**
```bash
export SKILLPOD_ENABLED_SKILLS=hello-world,code-review,my-namespace/my-skill
```

**Filter by namespace:**
```bash
export SKILLPOD_ENABLED_NAMESPACES=my-tools,team-skills
```

## Per-Client Setup

Run different SkillPod configurations for different AI agents:

```json
{
  "mcpServers": {
    "skillpod-dev": {
      "command": "uv",
      "args": ["run", "skillpod-mcp"],
      "env": {
        "SKILLPOD_SKILLS_DIR": "~/.skillpod/skills",
        "SKILLPOD_ENABLED_CATEGORIES": "development,testing"
      }
    },
    "skillpod-writing": {
      "command": "uv",
      "args": ["run", "skillpod-mcp"],
      "env": {
        "SKILLPOD_SKILLS_DIR": "~/.skillpod/skills",
        "SKILLPOD_ENABLED_CATEGORIES": "writing,research"
      }
    }
  }
}
```

This gives each AI agent a different view of the same skill repository.

## GitHub Integration

### Authentication

Set `GITHUB_TOKEN` for:
- Private repository access
- Higher rate limits (5,000 req/hour vs 60 req/hour)

```bash
export GITHUB_TOKEN=ghp_xxxxx
```

### Supported URL Formats

```bash
# Repository root
skillpod add https://github.com/user/repo

# Specific directory (branch/tag)
skillpod add https://github.com/user/repo/tree/main/skills/my-skill

# Specific directory (commit)
skillpod add https://github.com/user/repo/tree/abc123/path/to/skill
```

### Security Limits

| Limit | Value |
|-------|-------|
| Max file size | 1 MB |
| Max total extracted | 10 MB |
| Symlinks | Rejected |
| Hidden files | Rejected |

## Index Management

### Automatic Reindexing

SkillPod automatically reindexes when:
- Skills directory content changes (hash-based detection)
- Schema version changes
- Embedding provider changes

### Manual Reindexing

```bash
# Force reindex on server start
skillpod serve --reindex

# Skip auto-reindex check
skillpod serve --skip-auto-reindex
```

### Index Location

| SKILLS_DIR | Index Location |
|------------|----------------|
| Default (`~/.skillpod/skills`) | `~/.skillpod/indexes/default/` |
| Custom path | `~/.skillpod/indexes/{hash}/` |

## MCP Client Configuration

### Cursor

[![Install MCP Server](https://cursor.com/deeplink/mcp-install-dark.svg)](cursor://anysphere.cursor-deeplink/mcp/install?name=skillpod&config=eyJjb21tYW5kIjoidXYiLCJhcmdzIjpbInJ1biIsInNraWxscG9kLW1jcCJdLCJlbnYiOnsiU0tJTExQT0RfU0tJTExTX0RJUiI6In4vLnNraWxscG9kL3NraWxscyJ9fQ==)

Or manually add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "skillpod": {
      "command": "uv",
      "args": ["run", "skillpod-mcp"],
      "env": { "SKILLPOD_SKILLS_DIR": "~/.skillpod/skills" }
    }
  }
}
```

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "skillpod": {
      "command": "uv",
      "args": ["run", "skillpod-mcp"],
      "env": { "SKILLPOD_SKILLS_DIR": "~/.skillpod/skills" }
    }
  }
}
```

### Windsurf

Add to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "skillpod": {
      "command": "uv",
      "args": ["run", "skillpod-mcp"],
      "env": { "SKILLPOD_SKILLS_DIR": "~/.skillpod/skills" }
    }
  }
}
```

### Claude Code

```bash
claude mcp add skillpod -- uv run skillpod-mcp
# With custom skills directory:
claude mcp add --env SKILLPOD_SKILLS_DIR=~/.skillpod/skills skillpod -- uv run skillpod-mcp
```

### Kiro

[![Add to Kiro](https://kiro.dev/images/add-to-kiro.svg)](https://kiro.dev/launch/mcp/add?name=skillpod&config=%7B%22command%22%3A%20%22uv%22%2C%20%22args%22%3A%20%5B%22run%22%2C%20%22skillpod-mcp%22%5D%2C%20%22env%22%3A%20%7B%22SKILLPOD_SKILLS_DIR%22%3A%20%22~/.skillpod/skills%22%7D%2C%20%22disabled%22%3A%20false%2C%20%22autoApprove%22%3A%20%5B%5D%7D)

## See Also

- [CLI Reference](cli.md) — Command documentation
- [Creating Skills](creating-skills.md) — SKILL.md format
- [Design Philosophy](philosophy.md) — Why things work this way
