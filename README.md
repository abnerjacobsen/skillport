# SkillPod MCP

<div align="center">

**Search, Scope, Share — Agent Skills for Every MCP Client**

Hybrid search across 100+ skills. Scoped access per agent. Works everywhere.

[![MCP](https://img.shields.io/badge/MCP-Enabled-green)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

</div>

## Why SkillPod?

[Agent Skills](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview) bring **progressive disclosure** to AI agents — expert knowledge loads only when needed. SkillPod brings this to the MCP ecosystem with **search** and **scoping**.

| Challenge | SkillPod Solution |
|-----------|-------------------|
| Skills only work in Claude Code | MCP-native — works with Cursor, Windsurf, Copilot, any MCP client |
| 100+ skills bloat system prompts | Hybrid search — agents find and load only what they need |
| Same skills for every agent | Scoped access — dev tools for IDE, writing skills for chat |
| Manual skill installation | One command — `skillpod add https://github.com/...` |

```
        IDEs                    Chat                    CLI
┌─────────────────┐     ┌───────────────┐     ┌─────────────────┐
│ Cursor, Windsurf│     │Claude Desktop │     │ Claude Code     │
│ Copilot, Kiro   │     │  Claude.ai    │     │ Codex, Gemini   │
└────────┬────────┘     └───────┬───────┘     └────────┬────────┘
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                │ MCP
                         ┌──────▼──────┐
                         │  SkillPod   │  search → load → execute
                         └──────┬──────┘
                                │
                         ┌──────▼──────┐
                         │ SKILLS_DIR  │  Git repo, local folder,
                         └─────────────┘  or shared drive
```

## Quick Start

### 1. Install

**Cursor** (one-click)

[![Install MCP Server](https://cursor.com/deeplink/mcp-install-dark.svg)](cursor://anysphere.cursor-deeplink/mcp/install?name=skillpod&config=eyJjb21tYW5kIjoidXYiLCJhcmdzIjpbInJ1biIsInNraWxscG9kLW1jcCJdLCJlbnYiOnsiU0tJTExTX0RJUiI6In4vLnNraWxscG9kL3NraWxscyJ9fQ==)

**Kiro** (one-click)

[![Add to Kiro](https://kiro.dev/images/add-to-kiro.svg)](https://kiro.dev/launch/mcp/add?name=skillpod&config=%7B%22command%22%3A%20%22uv%22%2C%20%22args%22%3A%20%5B%22run%22%2C%20%22skillpod-mcp%22%5D%2C%20%22env%22%3A%20%7B%22SKILLS_DIR%22%3A%20%22~/.skillpod/skills%22%7D%2C%20%22disabled%22%3A%20false%2C%20%22autoApprove%22%3A%20%5B%5D%7D)

**Other Clients**

```json
{
  "mcpServers": {
    "skillpod": {
      "command": "uv",
      "args": ["run", "skillpod-mcp"],
      "env": { "SKILLS_DIR": "~/.skillpod/skills" }
    }
  }
}
```

<details>
<summary>Config file locations</summary>

- **Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windsurf**: `~/.codeium/windsurf/mcp_config.json`
- **Claude Code**: `claude mcp add skillpod -- uv run skillpod-mcp`

</details>

### 2. Add Your First Skill

```bash
skillpod add hello-world
```

### 3. Use It

Ask your AI: *"Search for hello-world and run it"*

The agent will:
1. `search_skills("hello-world")` — find matching skills
2. `load_skill("hello-world")` — get instructions + path
3. Follow the instructions using its tools

## Core Features

### Hybrid Search

Find skills by intent, not exact keywords. Full-text search works out of the box; add OpenAI/Gemini for vector search.

```bash
# Search by description
search_skills("code review checklist")

# List all skills
search_skills("")
```

### Scoped Access

Expose different skills to different agents:

```json
{
  "mcpServers": {
    "skillpod-dev": {
      "env": { "SKILLPOD_ENABLED_CATEGORIES": "development,testing" }
    },
    "skillpod-writing": {
      "env": { "SKILLPOD_ENABLED_SKILLS": "summarizer,translator" }
    }
  }
}
```

### GitHub Integration

Install skills directly from GitHub:

```bash
skillpod add https://github.com/user/repo/tree/main/skills/code-review
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `SKILLS_DIR` | Skills directory | `~/.skillpod/skills` |
| `EMBEDDING_PROVIDER` | `none`, `openai`, `gemini` | `none` |

[Full Configuration Guide →](guide/configuration.md)

## CLI

```bash
skillpod add <source>      # Add skills (local, GitHub, built-in)
skillpod list              # List installed skills
skillpod remove <id>       # Remove a skill
skillpod lint              # Validate skills
```

[CLI Reference →](guide/cli.md)

## Creating Skills

```markdown
---
name: my-skill
description: What this skill does
---
# My Skill

Instructions for the AI agent.
```

[Skill Authoring Guide →](guide/creating-skills.md)

## MCP Tools

| Tool | Purpose |
|------|---------|
| `search_skills(query)` | Find skills by description |
| `load_skill(skill_id)` | Get full instructions and path |
| `read_skill_file(skill_id, path)` | Read templates/configs |

## Learn More

- [Configuration Guide](guide/configuration.md) — All options, filtering, multi-instance setup
- [CLI Reference](guide/cli.md) — Full command documentation
- [Creating Skills](guide/creating-skills.md) — SKILL.md format, best practices
- [Design Philosophy](guide/philosophy.md) — Why skills work this way

## Development

```bash
git clone https://github.com/gotalab/skillpod-mcp.git
cd skillpod-mcp
uv sync
SKILLS_DIR=.agent/skills uv run skillpod-mcp
```

## License

MIT
