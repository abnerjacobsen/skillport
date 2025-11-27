# Design Philosophy

This document explains the design principles behind SkillPod and Agent Skills.

## Why Skills?

### The Problem with System Prompts

Traditional approach to giving AI agents knowledge:

```
System Prompt (loaded every conversation):
├── Company guidelines (2,000 tokens)
├── Coding standards (3,000 tokens)
├── Review checklist (1,500 tokens)
├── 50 more instructions...
└── Total: 30,000+ tokens before you say "hello"
```

**Problems:**
- Context window bloat
- Irrelevant knowledge in every conversation
- Hard to maintain and update
- No way to share across teams

### The Skills Solution

Skills use **progressive disclosure** - load knowledge only when relevant:

```
Conversation start:
├── Skill metadata only (~100 tokens each)
└── Full instructions loaded on demand

User: "Review this PR"
├── Agent searches: "code review"
├── Loads: code-review skill (1,500 tokens)
└── Uses only what's needed
```

## Skills vs MCP

A common question: "Isn't this what MCP does?"

| Layer | Role | Example |
|-------|------|---------|
| **MCP** | Data access | "Connect to GitHub API" |
| **Skills** | Procedural knowledge | "When reviewing PRs, check these 5 things" |

> MCP connects to data. Skills teach *how to use* that data.

**They're complementary:**
```
MCP Server: Provides GitHub API access
    ↓
Skill: "When reviewing PRs on GitHub:
        1. Check CI status first
        2. Look for security issues
        3. Verify test coverage..."
```

## Why SkillPod?

Claude Code has built-in Skills support (`.claude/skills/`), but:

| Feature | Claude Code | SkillPod |
|---------|-------------|----------|
| Client support | Claude Code only | Any MCP client |
| Search | Basic matching | Hybrid vector + FTS |
| Filtering | None | By category/namespace/skill |
| Installation | Manual copy | CLI + GitHub integration |
| Scaling | Limited | 100+ skills efficiently |

SkillPod brings Skills to **every MCP client** with search and scoping.

## Progressive Disclosure

Skills load information in stages:

| Stage | When Loaded | Token Cost | Content |
|-------|-------------|------------|---------|
| **Level 1** | Server start | ~100/skill | Name + description (metadata) |
| **Level 2** | `load_skill()` | < 5,000 | Full instructions (SKILL.md body) |
| **Level 3** | `read_skill_file()` | Variable | Templates, configs, references |

```
100 skills installed:
├── Level 1: 100 × ~100 = ~10,000 tokens (metadata only)
├── Level 2: Load 1-2 relevant skills = ~5,000 tokens
└── Total: ~15,000 tokens vs 300,000+ if all loaded
```

## Path-Based Design

### Skills Are Knowledge, Not Execution Environments

```
┌─────────────────────────────────────────────────────────────┐
│ User's Project (Agent's execution context)                  │
│                                                             │
│  ├── src/            ← Code generation                      │
│  ├── output/         ← Script outputs                       │
│  └── .venv/          ← Execution environment                │
│                                                             │
│  【Agent executes here】                                    │
└─────────────────────────────────────────────────────────────┘
                    ↑
          Agent uses skill knowledge
          to work in user's project
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ SkillPod MCP Server                                         │
│                                                             │
│  ├── search_skills()   → Find relevant skills               │
│  ├── load_skill()      → Get instructions + path            │
│  └── read_skill_file() → Read templates if needed           │
│                                                             │
│  【Knowledge provider, not execution environment】          │
└─────────────────────────────────────────────────────────────┘
```

### Why Return Paths Instead of Content?

```python
# load_skill returns:
{
    "name": "pdf-extractor",
    "instructions": "...",
    "path": "/Users/me/.skillpod/skills/pdf-extractor"
}
```

The agent uses `path` to execute scripts:

```bash
# Agent runs in user's project:
python /Users/me/.skillpod/skills/pdf-extractor/scripts/extract.py \
    ./input.pdf \
    --output ./output/extracted.txt
```

**Benefits:**

| Approach | Context Cost | Output Location | File Transfer |
|----------|--------------|-----------------|---------------|
| Return file content | High (code in context) | MCP server | Needed |
| Return path | Low (~20 tokens) | User's project | Not needed |

### Context Engineering

The key insight: **executing code doesn't require reading code**.

```
❌ Inefficient:
1. read_skill_file("pdf", "scripts/extract.py")  → 2,000 tokens
2. Look at the code
3. Execute it anyway

✅ Efficient:
1. load_skill("pdf")  → Get path
2. Execute: python {path}/scripts/extract.py  → 20 tokens
```

**When to read file content:**
- Need to understand the code
- Want to modify or adapt it
- Debugging issues

**When to use path only:**
- Just executing a working script
- Running validated tools

## Scoped Access

Different agents need different skills:

```
IDE Agent (Cursor, Windsurf):
├── code-review
├── testing
├── refactoring
└── debugging

Chat Agent (Claude Desktop):
├── writing-assistant
├── summarizer
├── translator
└── research
```

SkillPod enables this via filtering:

```json
{
  "mcpServers": {
    "skillpod-ide": {
      "env": { "SKILLPOD_ENABLED_CATEGORIES": "development" }
    },
    "skillpod-chat": {
      "env": { "SKILLPOD_ENABLED_CATEGORIES": "writing,research" }
    }
  }
}
```

Same skill repository, different views per agent.

## Design Principles

### 1. Convention Over Configuration

```bash
# Just works with defaults
skillpod add hello-world
skillpod  # starts server
```

Configuration only when you need to customize.

### 2. Progressive Complexity

| Level | User | Features |
|-------|------|----------|
| Basic | "I want to try skills" | `add`, `list`, defaults |
| Intermediate | "I have many skills" | Categories, namespaces |
| Advanced | "I need fine control" | Filtering, multi-instance, embedding |

### 3. Portable Format

Skills use Claude's Agent Skills format:
- Works with Claude Code natively
- Works with any MCP client via SkillPod
- Plain Markdown + YAML (no lock-in)

### 4. Searchable by Default

Every skill is searchable without configuration:
- FTS works out of the box
- Vector search optional (needs API key)
- Fallback chain ensures results

## Trade-offs

### What We Chose

| Decision | Trade-off | Rationale |
|----------|-----------|-----------|
| FTS default | Less semantic matching | No API keys, privacy, speed |
| Path-based | Agent needs shell access | Context efficiency, direct output |
| 2-level nesting | Limited hierarchy | Simplicity, covers 95% of cases |
| No version lock | Manual updates | Simplicity, skills are usually small |

### What We Avoided

- **Central registry**: Added complexity, governance overhead
- **Dependency resolution**: Skills should be self-contained
- **Hot reload**: Complexity for rare use case
- **Deep nesting**: Diminishing returns after 2 levels

## See Also

- [Creating Skills](creating-skills.md) - Practical skill authoring
- [Configuration](configuration.md) - Filtering and scoping options
- [Internal Design Docs](../docs/latest/SKILL_PHILOSOPHY.md) - Detailed rationale
