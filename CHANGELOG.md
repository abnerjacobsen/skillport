# Changelog
All notable changes to this project will be documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and [Semantic Versioning](https://semver.org/).

## [0.0.1](https://github.com/gotalab/skillhub-mcp/compare/v0.0.0...v0.0.1) (2025-11-26)


### Features

* **ci:** migrate from semantic-release to Release Please ([bf8ce99](https://github.com/gotalab/skillhub-mcp/commit/bf8ce9922fd654cc789308c311dba0756419de47))


### Bug Fixes

* **ci:** exclude only tasks/AGENTS.md from release snapshot ([597e4cc](https://github.com/gotalab/skillhub-mcp/commit/597e4ccc0560a24b5de07395c03d476e72cb201d))
* **ci:** exclude tasks/ directory from release snapshot ([003bbc6](https://github.com/gotalab/skillhub-mcp/commit/003bbc6d9d880c1c786488c212df1c9268987299))
* **tests:** update test for uv run python command ([77babc2](https://github.com/gotalab/skillhub-mcp/commit/77babc2d239dd5ed5e67272ae4102e9e2c3fb4a0))


### Documentation

* update release documentation for Release Please ([04c06dd](https://github.com/gotalab/skillhub-mcp/commit/04c06dd4091500b3403d21861aba060ca40775ac))


### Miscellaneous Chores

* trigger v0.0.1 release ([569e86e](https://github.com/gotalab/skillhub-mcp/commit/569e86ed322be795ee2b448e33b6da39df04fe2a))

## [Unreleased]
- Add GitHub Actions workflow for tag-driven releases (docs snapshot + changelog update + verify).
- Optional: add behavioral regression tests (golden traces) to release gate.
- Clarify branding (SkillHub) vs package/CLI name (`skillhub-mcp`) and add CLI alias `skillhub`.

## [0.0.0] - 2025-11-23
### Added
- Initial MCP server with search/load/read/execute tools.
- FTS-based search with category/tags normalization and fallbacks.
- English guides: AGENTS (core), ENGINEERING_GUIDE, RUNBOOK, VERSIONING.

### Changed
- Default `EMBEDDING_PROVIDER=none`; search defaults `limit=10`, `threshold=0.3`.

### Security
- Path traversal guards, command allowlist + timeout.
- Logging to stderr only (stdout reserved for JSON-RPC).

<!-- Links -->
[Unreleased]: https://github.com/gota/skillhub-mcp/compare/v0.0.0...HEAD
[0.0.0]: https://github.com/gota/skillhub-mcp/releases/tag/v0.0.0
