# CLI Reference

SkillPod provides a command-line interface for managing skills and running the MCP server.

## Overview

```bash
skillpod <command> [options]
```

> **Note**: `skillpod` is an alias for `skillpod-mcp`. Both work identically.

## Commands

### skillpod add

Add skills from various sources.

```bash
skillpod add <source> [options]
```

#### Sources

| Type | Example | Description |
|------|---------|-------------|
| Built-in | `hello-world` | Sample skill bundled with SkillPod |
| Built-in | `template` | Starter template for creating skills |
| Local | `./my-skill/` | Single skill directory |
| Local | `./my-collection/` | Directory containing multiple skills |
| GitHub | `https://github.com/user/repo` | Repository root |
| GitHub | `https://github.com/user/repo/tree/main/skills` | Specific directory |

#### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--dir <path>` | Target skills directory | `$SKILLS_DIR` or `~/.skillpod/skills` |
| `--force` | Overwrite existing skills without confirmation | `false` |
| `--keep-structure` | Preserve directory structure as namespace | `false` |
| `--flat` | Flatten directory structure (default for multi-skill) | `true` |
| `--namespace <name>` | Custom namespace for multi-skill sources | source directory name |
| `--name <name>` | Override skill name (single skill only) | from SKILL.md |

#### Examples

**Built-in skills:**
```bash
# Add sample skill
skillpod add hello-world

# Add template for creating your own
skillpod add template
```

**Local directory:**
```bash
# Single skill
skillpod add ./my-skill/

# Multiple skills - flatten (default)
skillpod add ./my-collection/
# → skills/skill-a/, skills/skill-b/, skills/skill-c/

# Multiple skills - preserve structure
skillpod add ./my-collection/ --keep-structure
# → skills/my-collection/skill-a/, skills/my-collection/skill-b/

# Multiple skills - custom namespace
skillpod add ./my-collection/ --namespace team-tools
# → skills/team-tools/skill-a/, skills/team-tools/skill-b/
```

**GitHub:**
```bash
# Specific skill from repository
skillpod add https://github.com/user/repo/tree/main/skills/code-review

# All skills from repository
skillpod add https://github.com/user/repo

# Force overwrite existing
skillpod add https://github.com/user/repo/tree/main/skill --force
```

**Custom directory:**
```bash
skillpod add hello-world --dir ~/work/project/.skills
```

#### Interactive Mode

When adding multiple skills without `--flat` or `--keep-structure`, you'll be prompted:

```
Found 3 skills:
  - code-review
  - testing
  - documentation

How to add?
  [1] Flat    → skills/code-review/, skills/testing/, ...
  [2] Grouped → skills/my-collection/code-review/, ...
  [3] Custom namespace
  [0] Cancel

Choice [1]:
```

---

### skillpod list

List installed skills.

```bash
skillpod list [options]
```

#### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--dir <path>` | Skills directory to list | `$SKILLS_DIR` |
| `--category <cat>` | Filter by category | all |
| `--id-prefix <prefix>` | Filter by ID prefix (namespace) | all |
| `--json` | Output as JSON | `false` |

#### Examples

```bash
# List all skills (tree view)
skillpod list

# Filter by category
skillpod list --category development

# Filter by namespace
skillpod list --id-prefix team-tools/

# JSON output for scripting
skillpod list --json
```

#### Output Format

**Default (tree view):**
```
Skills in ~/.skillpod/skills/

hello-world
  description: A simple hello world skill
  category: example

team-tools/
  code-review
    description: Code review checklist
    category: development
  testing
    description: Testing guidelines
    category: development
```

**JSON:**
```json
{
  "skills": [
    {
      "id": "hello-world",
      "name": "hello-world",
      "description": "A simple hello world skill",
      "category": "example"
    },
    {
      "id": "team-tools/code-review",
      "name": "code-review",
      "description": "Code review checklist",
      "category": "development"
    }
  ]
}
```

---

### skillpod remove

Remove installed skills.

```bash
skillpod remove <skill-id> [options]
```

#### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--dir <path>` | Skills directory | `$SKILLS_DIR` |
| `--force` | Skip confirmation | `false` |

#### Examples

```bash
# Remove with confirmation
skillpod remove hello-world
# → Remove 'hello-world'? [y/N]

# Remove without confirmation
skillpod remove hello-world --force

# Remove namespaced skill
skillpod remove team-tools/code-review
```

---

### skillpod lint

Validate skill files.

```bash
skillpod lint [skill-id] [options]
```

#### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--dir <path>` | Skills directory | `$SKILLS_DIR` |

#### Examples

```bash
# Lint all skills
skillpod lint

# Lint specific skill
skillpod lint hello-world

# Lint namespaced skill
skillpod lint team-tools/code-review
```

#### Output

```
Validating skills in ~/.skillpod/skills/

hello-world
  ✓ Valid

team-tools/code-review
  ✓ Valid

broken-skill
  ✗ name 'wrong-name' does not match directory 'broken-skill'
  ✗ description is required

2/3 skills valid
```

---

### Server Mode

Start the MCP server.

```bash
skillpod [options]
```

#### Options

| Option | Description |
|--------|-------------|
| `--reindex` | Force reindex on startup |
| `--skip-auto-reindex` | Skip automatic reindex check |

#### Examples

```bash
# Start server (normal)
skillpod

# Start with forced reindex
skillpod --reindex

# Start without auto-reindex check
skillpod --skip-auto-reindex
```

---

## Global Options

These options work with most commands:

| Option | Description |
|--------|-------------|
| `--dir <path>` | Override skills directory |
| `--help` | Show help |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (invalid input, not found, etc.) |

## Environment Variables

CLI commands respect these environment variables:

| Variable | Description |
|----------|-------------|
| `SKILLS_DIR` | Default skills directory |
| `GITHUB_TOKEN` | GitHub authentication for private repos |

See [Configuration Guide](configuration.md) for all options.
