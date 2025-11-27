# 📦 SkillSouko

<div align="center">

🏭 **Your Agent Skills Warehouse** · *Skill + 倉庫 (Souko)* 📦

A centralized hub to install, organize, and distribute Agent Skills to any MCP client.

[![MCP](https://img.shields.io/badge/MCP-Enabled-green)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

</div>

## What are Agent Skills?

[Agent Skills](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview) are folders of instructions, scripts, and resources that AI agents load on demand. Instead of cramming everything into a system prompt, skills let agents search for and load only what they need.

**SkillSouko** brings Agent Skills to any MCP-compatible client (Cursor, Windsurf, Claude Desktop, etc.) with full lifecycle management.

## Why SkillSouko?

| Need | SkillSouko Solution |
|------|-------------------|
| Use Agent Skills in Cursor/Windsurf | MCP server delivers skills to any client |
| Add skills from GitHub | `skillsouko add https://github.com/...` |
| Organize by team or project | Categories and namespaces |
| Different skills for different clients | Filter by category, namespace, or skill ID |
| Scale to 100+ skills | FTS search + optional vector search |

```
┌─────────────────────────────────────────────┐
│  Your AI Agent (Cursor, Windsurf, etc.)     │
└──────────────────────┬──────────────────────┘
                       │ MCP
              ┌────────▼────────┐
              │    SkillSouko     │
              │  search → load  │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │   Your Skills   │
              │ (GitHub, local) │
              └─────────────────┘
```

## Quick Start

### 1. Install

**Cursor** (one-click)

[![Install MCP Server](https://cursor.com/deeplink/mcp-install-dark.svg)](cursor://anysphere.cursor-deeplink/mcp/install?name=skillsouko&config=eyJjb21tYW5kIjoidXYiLCJhcmdzIjpbInJ1biIsInNraWxscG9kLW1jcCJdLCJlbnYiOnsiU0tJTExQT0RfU0tJTExTX0RJUiI6In4vLnNraWxscG9kL3NraWxscyJ9fQ==)

**Kiro** (one-click)

[![Add to Kiro](https://kiro.dev/images/add-to-kiro.svg)](https://kiro.dev/launch/mcp/add?name=skillsouko&config=%7B%22command%22%3A%20%22uv%22%2C%20%22args%22%3A%20%5B%22run%22%2C%20%22skillsouko-mcp%22%5D%2C%20%22env%22%3A%20%7B%22SKILLSOUKO_SKILLS_DIR%22%3A%20%22~/.skillsouko/skills%22%7D%2C%20%22disabled%22%3A%20false%2C%20%22autoApprove%22%3A%20%5B%5D%7D)

**Other Clients**

```json
{
  "mcpServers": {
    "skillsouko": {
      "command": "uv",
      "args": ["run", "skillsouko-mcp"],
      "env": { "SKILLSOUKO_SKILLS_DIR": "~/.skillsouko/skills" }
    }
  }
}
```

<details>
<summary>Config file locations</summary>

- **Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windsurf**: `~/.codeium/windsurf/mcp_config.json`
- **Claude Code**: `claude mcp add skillsouko -- uv run skillsouko-mcp`

</details>

### 2. Add Your First Skill

```bash
skillsouko add hello-world
```

### 3. Use It

Ask your AI: *"Search for hello-world and run it"*

The agent will:
1. `search_skills("hello-world")` — find matching skills
2. `load_skill("hello-world")` — get instructions + path
3. Follow the instructions using its tools

## Key Features

### Deliver: MCP Server

Three tools for progressive skill loading:

| Tool | Purpose |
|------|---------|
| `search_skills(query)` | Find skills by task description |
| `load_skill(skill_id)` | Get full instructions and filesystem path |
| `read_skill_file(skill_id, path)` | Read templates and configs |

### Manage: CLI

Full lifecycle management from the command line:

```bash
skillsouko add <source>      # GitHub URL, local path, or built-in name
skillsouko list              # See installed skills
skillsouko search <query>    # Find skills by description
skillsouko show <id>         # View skill details
skillsouko lint [id]         # Validate skill files
skillsouko remove <id>       # Uninstall a skill
```

**GitHub Integration:**

```bash
# Add from GitHub
skillsouko add https://github.com/user/repo/tree/main/skills/code-review

# Add entire repository
skillsouko add https://github.com/user/repo
```

### Organize: Categories & Namespaces

Structure your skills and control what each client sees:

```yaml
# SKILL.md frontmatter
metadata:
  skillsouko:
    category: development
    tags: [testing, quality]
    alwaysApply: true  # Core Skills - always available
```

**Client-Based Skill Filtering:**

Expose different skills to different AI agents:

```json
{
  "mcpServers": {
    "skillsouko-development": {
      "command": "uv",
      "args": ["run", "skillsouko-mcp"],
      "env": { "SKILLSOUKO_ENABLED_CATEGORIES": "development,testing" }
    }
  }
}
```


```json
{
  "mcpServers": {
    "writing-skills": {
      "command": "uv",
      "args": ["run", "skillsouko-mcp"],
      "env": { "SKILLSOUKO_ENABLED_CATEGORIES": "writing,research" }
    }
  }
}
```

Filter options:
- `SKILLSOUKO_ENABLED_SKILLS` — Specific skill IDs
- `SKILLSOUKO_ENABLED_CATEGORIES` — By category
- `SKILLSOUKO_ENABLED_NAMESPACES` — By directory prefix

### Scale: Smart Search

**Full-Text Search (Default)**

Works out of the box with no API keys. BM25-based search via Tantivy indexes skill names, descriptions, tags, and categories.

```bash
# No configuration needed
SKILLSOUKO_EMBEDDING_PROVIDER=none  # default
```

**Vector Search (Optional)**

For semantic search across large skill collections:

```bash
# OpenAI
export SKILLSOUKO_EMBEDDING_PROVIDER=openai
export OPENAI_API_KEY=sk-...

# Gemini
export SKILLSOUKO_EMBEDDING_PROVIDER=gemini
export GEMINI_API_KEY=...
```

**Fallback Chain**: vector → FTS → substring (always returns results)

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `SKILLSOUKO_SKILLS_DIR` | Skills directory | `~/.skillsouko/skills` |
| `SKILLSOUKO_EMBEDDING_PROVIDER` | `none`, `openai`, or `gemini` | `none` |

[Full Configuration Guide →](guide/configuration.md)

## Creating Skills

```markdown
---
name: my-skill
description: What this skill does
metadata:
  skillsouko:
    category: development
    tags: [example]
---
# My Skill

Instructions for the AI agent.
```

[Skill Authoring Guide →](guide/creating-skills.md)

## Learn More

- [Configuration Guide](guide/configuration.md) — Filtering, search options, multi-client setup
- [Creating Skills](guide/creating-skills.md) — SKILL.md format and best practices
- [CLI Reference](guide/cli.md) — Full command documentation
- [Design Philosophy](guide/philosophy.md) — Why skills work this way

## Development

```bash
git clone https://github.com/gotalab/skillsouko.git
cd skillsouko
uv sync
SKILLSOUKO_SKILLS_DIR=.agent/skills uv run skillsouko serve
```

## License

MIT
