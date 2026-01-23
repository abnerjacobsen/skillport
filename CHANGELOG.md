# Changelog

## [0.1.4](https://github.com/abnerjacobsen/skillport/compare/v1.1.1...v0.1.4) (2026-01-23)


### ⚠ BREAKING CHANGES

* CLI and MCP server are now separate packages.

### Features

* add `skillhub add` command and use ~/.skillhub/ as default ([#5](https://github.com/abnerjacobsen/skillport/issues/5)) ([ea16ed4](https://github.com/abnerjacobsen/skillport/commit/ea16ed463ec34602ced7cdb6be154a688b391ef8))
* add Codex skills directory option to init command ([#29](https://github.com/abnerjacobsen/skillport/issues/29)) ([9d44f6e](https://github.com/abnerjacobsen/skillport/commit/9d44f6e0d5305936ba7d32a6b21d96e16f5772c0))
* add GitHub shorthand format for add command ([#50](https://github.com/abnerjacobsen/skillport/issues/50)) ([4b0700d](https://github.com/abnerjacobsen/skillport/commit/4b0700d1ad0f22b8dbb361615cd99bdd7e9915a2))
* add init flag to skip instruction updates ([#69](https://github.com/abnerjacobsen/skillport/issues/69)) ([ed8054e](https://github.com/abnerjacobsen/skillport/commit/ed8054ede3c2bc8b6f50a5f3f7366626d851f8c3))
* add location element and proper XML format for skill-client-integration spec compliance ([#42](https://github.com/abnerjacobsen/skillport/issues/42)) ([c052a45](https://github.com/abnerjacobsen/skillport/commit/c052a45f5419f2a4aec2c2c510c81606f3fdb317))
* add metadata CLI commands ([#60](https://github.com/abnerjacobsen/skillport/issues/60)) ([2969cd8](https://github.com/abnerjacobsen/skillport/commit/2969cd8fd4679c37ecbcf6cfdada59691bebb226))
* Add multi-client support, skill scoping, and context-efficient skill loading with updated documentation and tests. ([4c2ddb7](https://github.com/abnerjacobsen/skillport/commit/4c2ddb71dea4d83ac6f614bb454d1ec3b325f8b6))
* add namespace filtering and custom add options ([#7](https://github.com/abnerjacobsen/skillport/issues/7)) ([e8970e5](https://github.com/abnerjacobsen/skillport/commit/e8970e54427f492e14b5e0cfa2aa86fbeadb0811))
* add namespace filtering, custom add options, and origin tracking ([9e846fd](https://github.com/abnerjacobsen/skillport/commit/9e846fdb6817d30b2e201c8d8bc3078a4f26826a))
* add skill update command and configure ruff linting ([#26](https://github.com/abnerjacobsen/skillport/issues/26)) ([c6f0ab9](https://github.com/abnerjacobsen/skillport/commit/c6f0ab922c46216d51b1d9b730bf044f9863bd8a))
* add skill-evaluator skill ([591ccbe](https://github.com/abnerjacobsen/skillport/commit/591ccbe803376e6f73f4be2a02bb104afceed1a3))
* add validation rules for reserved words, XML tags, and type checks ([#54](https://github.com/abnerjacobsen/skillport/issues/54)) ([5e41fb2](https://github.com/abnerjacobsen/skillport/commit/5e41fb2b6302a672f16b81b0e0ca2da35485bffe))
* add zip file support for skill installation ([#37](https://github.com/abnerjacobsen/skillport/issues/37)) ([0b9fce4](https://github.com/abnerjacobsen/skillport/commit/0b9fce41cf315605c2aabc4ac8908948b7bafae2))
* auto-detect GitHub auth via gh CLI ([#48](https://github.com/abnerjacobsen/skillport/issues/48)) ([758ac1f](https://github.com/abnerjacobsen/skillport/commit/758ac1f6ae442dd270805fef94ac9a7164cad119))
* **ci:** migrate from semantic-release to Release Please ([3e11f85](https://github.com/abnerjacobsen/skillport/commit/3e11f85a46f7705b36bb60da421a49d41772fddf))
* **cli:** add global skills/db overrides ([c6bd235](https://github.com/abnerjacobsen/skillport/commit/c6bd2352609202fa627b89f845a9ca0ca96fa087))
* **cli:** add global skills/db overrides ([a8d3c44](https://github.com/abnerjacobsen/skillport/commit/a8d3c44ccb5aa692156ec29b71060b97ae353883))
* derive db/meta per skills dir and improve add UX ([111889a](https://github.com/abnerjacobsen/skillport/commit/111889a386439225d8b9831ca06ed0e96283881b))
* Dynamically generate LanceDB path based on skills directory hash and update README with improved onboarding and architecture overview. ([48bb8fd](https://github.com/abnerjacobsen/skillport/commit/48bb8fdff3900c35b68994378eb771905b78376b))
* Enhance skill search and indexing with state management and a dedicated search service, and rename the `read_file` tool to `read_skill_file`. ([1fb139a](https://github.com/abnerjacobsen/skillport/commit/1fb139a2619cc497973c8db070963fcfbe9c974c))
* Implement skill readiness checks, automated setup, and status reporting with updated skill metadata and CLI commands. ([ea8b74f](https://github.com/abnerjacobsen/skillport/commit/ea8b74fe69a005b2566239ee3d0825a14c0bf72e))
* improve CLI and fix env var parsing for filters ([51e598d](https://github.com/abnerjacobsen/skillport/commit/51e598d3062054ab62973fa59238679e4faec3b7))
* Improve skill reindexing by skipping skills with non-mapping frontmatter and dropping the table when no valid skills are present. ([4ba5f8d](https://github.com/abnerjacobsen/skillport/commit/4ba5f8df12dc105d2b76dd30a78069e4a503bc68))
* initial release ([82cdaea](https://github.com/abnerjacobsen/skillport/commit/82cdaea69cfc22aa93307f94b0ef3be83131782b))
* Introduce `run_skill_command`, enhance `search_skills` with empty/wildcard query handling, and update execution environment documentation. ([0d010b5](https://github.com/abnerjacobsen/skillport/commit/0d010b5ccf33fc4fb14dc356610bcec47b24a499))
* **lead-research-assistant:** add new skill for identifying and qualifying leads ([8d187af](https://github.com/abnerjacobsen/skillport/commit/8d187af29b951217e8c6857c875d4cf2dc30f9b0))
* namespace filtering and CLI improvements ([cc1b988](https://github.com/abnerjacobsen/skillport/commit/cc1b988e34d7bf95132a9e70bfacd14ff3899435))
* propagate settings overrides, normalize skill prefilters, drop stale indexes, and refine search result limiting ([693015e](https://github.com/abnerjacobsen/skillport/commit/693015ed903229635901420220fd26d7afa1a2c1))
* Remove skill runtime and setup fields, and integrate uv for Python command execution. ([65fd58c](https://github.com/abnerjacobsen/skillport/commit/65fd58c78cd511a39ad0fb63c04cdb62e2175daa))
* show untracked skills in update command ([#31](https://github.com/abnerjacobsen/skillport/issues/31)) ([1e3a9dc](https://github.com/abnerjacobsen/skillport/commit/1e3a9dca8267eb14de804e951cad7fec2fa60098))
* show untracked skills in update command ([#34](https://github.com/abnerjacobsen/skillport/issues/34)) ([12873a1](https://github.com/abnerjacobsen/skillport/commit/12873a1c63805498ffa186c8d32cb74e7ca350a8))
* **validation:** add frontmatter validation rules ([d97fda4](https://github.com/abnerjacobsen/skillport/commit/d97fda4802275519eef742e6515897543d693b65))
* **validation:** add frontmatter validation rules ([1ba8884](https://github.com/abnerjacobsen/skillport/commit/1ba8884ccc81bad6f622a6429a89e0870431ad2d))


### Bug Fixes

* add Claude Code 2.1.0 frontmatter keys to validation and docs ([#74](https://github.com/abnerjacobsen/skillport/issues/74)) ([4680bf5](https://github.com/abnerjacobsen/skillport/commit/4680bf5e5e25464450d8cc0cdaa69adafdb6b6b3))
* align frontmatter validation with Agent Skills open standard ([#46](https://github.com/abnerjacobsen/skillport/issues/46)) ([0274cae](https://github.com/abnerjacobsen/skillport/commit/0274cae9aa1e760b66a1fa353a83816506781e22))
* auto reindex read commands ([230a729](https://github.com/abnerjacobsen/skillport/commit/230a729c56bb383bde4fa4c3f38b50a25bdcd323))
* change cli command sync to doc ([a28d95c](https://github.com/abnerjacobsen/skillport/commit/a28d95c4440392c824e4e6daa145cbf4f2efa380))
* change dir name ([5d75837](https://github.com/abnerjacobsen/skillport/commit/5d758376a1d5c5a721b63e02a807c5804927152e))
* **ci:** add manual publish trigger for PyPI ([#64](https://github.com/abnerjacobsen/skillport/issues/64)) ([1a63b38](https://github.com/abnerjacobsen/skillport/commit/1a63b38fdd304d67e9761659a27c9562311fb21c))
* **ci:** add write permission and push to main branch ([fe85f42](https://github.com/abnerjacobsen/skillport/commit/fe85f4257b5f0df5b3dbb3bb0a39189a62a0b675))
* **ci:** build packages by path in release workflow ([#62](https://github.com/abnerjacobsen/skillport/issues/62)) ([eafabcc](https://github.com/abnerjacobsen/skillport/commit/eafabcce2e249748a05b860df4853578e779aec2))
* **ci:** exclude only tasks/AGENTS.md from release snapshot ([4f4e558](https://github.com/abnerjacobsen/skillport/commit/4f4e558da3df055ea6f1157a3adddc0609bd99c1))
* **ci:** exclude tasks/ directory from release snapshot ([4117a02](https://github.com/abnerjacobsen/skillport/commit/4117a02113189809620a17ddfc6f2882d7679628))
* **ci:** remove unused snapshot-docs job ([#68](https://github.com/abnerjacobsen/skillport/issues/68)) ([f3457db](https://github.com/abnerjacobsen/skillport/commit/f3457db021b55aacb98882b3e00451da8e8c392a))
* **ci:** skip existing packages on PyPI upload ([#66](https://github.com/abnerjacobsen/skillport/issues/66)) ([86714f8](https://github.com/abnerjacobsen/skillport/commit/86714f87858eb8f0e5e9ce801a3c426d8d25f1c1))
* clean prefetched github temp dir after rename ([780cd5d](https://github.com/abnerjacobsen/skillport/commit/780cd5d5409bf1e09f0adfdb21152e7f516ff597))
* clean YAML frontmatter output ([#71](https://github.com/abnerjacobsen/skillport/issues/71)) ([40ccca6](https://github.com/abnerjacobsen/skillport/commit/40ccca6fab1f4edf0b8e8e08736ac9668b69aca2))
* **cli:** add Claude Code incompatibility warning for namespace option ([#40](https://github.com/abnerjacobsen/skillport/issues/40)) ([4951bdb](https://github.com/abnerjacobsen/skillport/commit/4951bdb72e466b010ecc5414e04ce71d144cd36a))
* **dev:** ensure skillport-mcp runnable after uv sync ([95b1c0b](https://github.com/abnerjacobsen/skillport/commit/95b1c0b8113e50b8db305d5f22265a8b8c72f6df))
* **dev:** ensure uv sync installs skillport-mcp for local MCP server runs ([750e42d](https://github.com/abnerjacobsen/skillport/commit/750e42d5d29f101185e4008f1a86bd13208d1128))
* **dev:** install skillport-mcp via uv default groups ([33526ac](https://github.com/abnerjacobsen/skillport/commit/33526ac8e67ca740eec2c26050bf1ac86857acd4))
* enforce strict frontmatter validation on add ([56e36e1](https://github.com/abnerjacobsen/skillport/commit/56e36e1df02f23705cbf7e23d067b2b2de961c60))
* enforce strict frontmatter validation on add ([b56fee9](https://github.com/abnerjacobsen/skillport/commit/b56fee94daf4ef105ba1d2fa469102c9ada21ce3))
* expand tilde paths cross-platform ([#61](https://github.com/abnerjacobsen/skillport/issues/61)) ([b10ba48](https://github.com/abnerjacobsen/skillport/commit/b10ba48b11a7b04ffd571c3316835d84cc73a6f3))
* harden path handling for cross-platform security ([#57](https://github.com/abnerjacobsen/skillport/issues/57)) ([192d448](https://github.com/abnerjacobsen/skillport/commit/192d4483400d346b5dbd7ddd5767f00367d14e5c))
* reuse fetched source and embedding defaults ([d250ea3](https://github.com/abnerjacobsen/skillport/commit/d250ea377676e8df4ae789b93b3db58d8963d658))
* support /blob/ format in GitHub URL parsing ([#58](https://github.com/abnerjacobsen/skillport/issues/58)) ([27cfe25](https://github.com/abnerjacobsen/skillport/commit/27cfe25c056e86f41c993be9022c09ab193e733d))
* **tests:** update test for uv run python command ([04086a6](https://github.com/abnerjacobsen/skillport/commit/04086a6e1277344614711eb8360fcc1a1495f3db))
* upgrade lancedb to 0.26.0 and fix deprecation warnings ([#44](https://github.com/abnerjacobsen/skillport/issues/44)) ([52911ae](https://github.com/abnerjacobsen/skillport/commit/52911ae18531482fc763fca45e53ed7bfcf6e40e))
* use Path.name for cross-platform directory extraction ([#52](https://github.com/abnerjacobsen/skillport/issues/52)) ([68b9f2f](https://github.com/abnerjacobsen/skillport/commit/68b9f2f9714d3209d950da511f323c3fc386d65a))
* use POSIX paths for cross-platform compatibility ([#35](https://github.com/abnerjacobsen/skillport/issues/35)) ([db7ad78](https://github.com/abnerjacobsen/skillport/commit/db7ad78cb878cbc51ca303a567f406a8b578b4fa))
* use raw FTS scores and fix scalar index  ([24442a9](https://github.com/abnerjacobsen/skillport/commit/24442a96873148150c797ffc46f364e2e2073b8d))
* use raw FTS scores and fix scalar index type ([9e04d26](https://github.com/abnerjacobsen/skillport/commit/9e04d26366e3aab4e0c11f54a7caf145ccab77ff))


### Reverts

* show untracked skills in update command ([6422fda](https://github.com/abnerjacobsen/skillport/commit/6422fdaa2326b003d0a7daa7264cc7a254d34f9b))


### Documentation

* add comprehensive guidelines for Terraform and OpenTofu usage ([f6e51cc](https://github.com/abnerjacobsen/skillport/commit/f6e51ccbd71ddd1719a1fbd677b783cdd573b51d))
* add comprehensive guidelines for versioning, refactoring, and best practices ([f6e51cc](https://github.com/abnerjacobsen/skillport/commit/f6e51ccbd71ddd1719a1fbd677b783cdd573b51d))
* add comprehensive guides for CI/CD, security, and version management ([f6e51cc](https://github.com/abnerjacobsen/skillport/commit/f6e51ccbd71ddd1719a1fbd677b783cdd573b51d))
* add Hugging Face Skills, remove SkillsMP Marketplace ([4f153cd](https://github.com/abnerjacobsen/skillport/commit/4f153cd0ac9c9582c6a81c30d0ab92b49fe0ca6c))
* add README in .agent/skills/ ([0ae05b5](https://github.com/abnerjacobsen/skillport/commit/0ae05b5d9d501ed077911f468de2217833b773f5))
* add README in .agent/skills/ ([f2d5523](https://github.com/abnerjacobsen/skillport/commit/f2d55238c11021cb480a56a7c86964eeea0681e2))
* add recommended community skills table to README ([913dc27](https://github.com/abnerjacobsen/skillport/commit/913dc27f498b8b1dc0d5dace2fb8311d977d2a2f))
* add recommended community skills table to README ([d40f04e](https://github.com/abnerjacobsen/skillport/commit/d40f04e5b6ef9f189fe93fceaf45e2b990f57748))
* add update command documentation and fix init example ([#30](https://github.com/abnerjacobsen/skillport/issues/30)) ([0c14b86](https://github.com/abnerjacobsen/skillport/commit/0c14b8695c4388c8f21ef7ff1d944d47ba5cbc4d))
* align config sample to AGENTS+GEMINI ([eb900b6](https://github.com/abnerjacobsen/skillport/commit/eb900b663c7d69d6210cde0664597d092d236bad))
* clarify CLI init/add flow ([495defa](https://github.com/abnerjacobsen/skillport/commit/495defa8a547c2173a585e8f17c9e2f4d21d5c4a))
* clarify CLI init/add flow ([0a4b887](https://github.com/abnerjacobsen/skillport/commit/0a4b88752bde7ce140bce4bd5874e8b1aff27918))
* clarify CLI init/add flow ([a0ff6b2](https://github.com/abnerjacobsen/skillport/commit/a0ff6b2b725b458e65f0ca50b80507423837e58c))
* mention Antigravity in other clients list ([99778c7](https://github.com/abnerjacobsen/skillport/commit/99778c78c68900575e7c93d67730d1e4feede01c))
* rebuild documentation structure ([fe77eb0](https://github.com/abnerjacobsen/skillport/commit/fe77eb005d8cff2c8d0be953b3d60f65aa584321))
* restore all documentation from 2f15525 ([b849349](https://github.com/abnerjacobsen/skillport/commit/b849349bfc0a53519e61b68b250590e296309d02))
* **terraform:** add advanced Terraform usage patterns and best practices ([f6e51cc](https://github.com/abnerjacobsen/skillport/commit/f6e51ccbd71ddd1719a1fbd677b783cdd573b51d))
* **terraform:** add CI/CD workflow reference for Terraform ([f6e51cc](https://github.com/abnerjacobsen/skillport/commit/f6e51ccbd71ddd1719a1fbd677b783cdd573b51d))
* **terraform:** add comprehensive code patterns and structure guide ([f6e51cc](https://github.com/abnerjacobsen/skillport/commit/f6e51ccbd71ddd1719a1fbd677b783cdd573b51d))
* **terraform:** add comprehensive Terraform skill guide ([1a8a468](https://github.com/abnerjacobsen/skillport/commit/1a8a46820df722717d7fe0cf2c3503b95ef4a9ab))
* **terraform:** add comprehensive Terraform skill guide ([f6e51cc](https://github.com/abnerjacobsen/skillport/commit/f6e51ccbd71ddd1719a1fbd677b783cdd573b51d))
* **terraform:** add detailed guide on testing frameworks ([f6e51cc](https://github.com/abnerjacobsen/skillport/commit/f6e51ccbd71ddd1719a1fbd677b783cdd573b51d))
* **terraform:** add module development patterns guide ([f6e51cc](https://github.com/abnerjacobsen/skillport/commit/f6e51ccbd71ddd1719a1fbd677b783cdd573b51d))
* **terraform:** add quick reference guide for terraform commands and workflows ([f6e51cc](https://github.com/abnerjacobsen/skillport/commit/f6e51ccbd71ddd1719a1fbd677b783cdd573b51d))
* **terraform:** add security and compliance reference guide ([f6e51cc](https://github.com/abnerjacobsen/skillport/commit/f6e51ccbd71ddd1719a1fbd677b783cdd573b51d))
* **testing:** add comprehensive guide on testing Terraform modules ([f6e51cc](https://github.com/abnerjacobsen/skillport/commit/f6e51ccbd71ddd1719a1fbd677b783cdd573b51d))
* translate guide to English and update CONTRIBUTING.md ([2387d25](https://github.com/abnerjacobsen/skillport/commit/2387d2506b52655d80b0270b29f76f11770563d2))
* translate guide to English and update CONTRIBUTING.md ([749c272](https://github.com/abnerjacobsen/skillport/commit/749c27260d14bceaaf086647294c8e38ecdef05a))
* update how to add codex skills ([4814997](https://github.com/abnerjacobsen/skillport/commit/4814997dbb2a2eedc711cc9412e4d5d24164fea2))


### Miscellaneous Chores

* prepare release ([2684deb](https://github.com/abnerjacobsen/skillport/commit/2684debe9b5bc4764afdd348e0d7e088a89e7c8f))
* set release package name ([6e63e66](https://github.com/abnerjacobsen/skillport/commit/6e63e666427930dc62baac842ea61070a29ded6a))
* trigger v0.0.1 release ([e02d59c](https://github.com/abnerjacobsen/skillport/commit/e02d59c960939810f03fa294c851b9d6747aa445))
* trigger v0.0.2 release ([3b01da2](https://github.com/abnerjacobsen/skillport/commit/3b01da2e384e0e36a94d754fd410d50ebea95e97))


### Code Refactoring

* split CLI and MCP server into separate distributions ([#56](https://github.com/abnerjacobsen/skillport/issues/56)) ([bb03e3a](https://github.com/abnerjacobsen/skillport/commit/bb03e3a374b1c47e073f47704b222836613cf1fc))

## [1.1.1](https://github.com/gotalab/skillport/compare/v1.1.0...v1.1.1) (2026-01-08)


### Bug Fixes

* add Claude Code 2.1.0 frontmatter keys to validation and docs ([#74](https://github.com/gotalab/skillport/issues/74)) ([4680bf5](https://github.com/gotalab/skillport/commit/4680bf5e5e25464450d8cc0cdaa69adafdb6b6b3))

## [1.1.0](https://github.com/gotalab/skillport/compare/v1.0.2...v1.1.0) (2025-12-29)


### Features

* add init flag to skip instruction updates ([#69](https://github.com/gotalab/skillport/issues/69)) ([ed8054e](https://github.com/gotalab/skillport/commit/ed8054ede3c2bc8b6f50a5f3f7366626d851f8c3))


### Bug Fixes

* clean YAML frontmatter output ([#71](https://github.com/gotalab/skillport/issues/71)) ([40ccca6](https://github.com/gotalab/skillport/commit/40ccca6fab1f4edf0b8e8e08736ac9668b69aca2))

## [1.0.2](https://github.com/gotalab/skillport/compare/v1.0.1...v1.0.2) (2025-12-28)


### Bug Fixes

* **ci:** add manual publish trigger for PyPI ([#64](https://github.com/gotalab/skillport/issues/64)) ([1a63b38](https://github.com/gotalab/skillport/commit/1a63b38fdd304d67e9761659a27c9562311fb21c))
* **ci:** remove unused snapshot-docs job ([#68](https://github.com/gotalab/skillport/issues/68)) ([f3457db](https://github.com/gotalab/skillport/commit/f3457db021b55aacb98882b3e00451da8e8c392a))
* **ci:** skip existing packages on PyPI upload ([#66](https://github.com/gotalab/skillport/issues/66)) ([86714f8](https://github.com/gotalab/skillport/commit/86714f87858eb8f0e5e9ce801a3c426d8d25f1c1))

## [1.0.1](https://github.com/gotalab/skillport/compare/v1.0.0...v1.0.1) (2025-12-28)


### Bug Fixes

* **ci:** build packages by path in release workflow ([#62](https://github.com/gotalab/skillport/issues/62)) ([eafabcc](https://github.com/gotalab/skillport/commit/eafabcce2e249748a05b860df4853578e779aec2))

## [1.0.0](https://github.com/gotalab/skillport/compare/v0.6.1...v1.0.0) (2025-12-28)


### ⚠ BREAKING CHANGES

* CLI and MCP server are now separate packages.

### Features

* add metadata CLI commands ([#60](https://github.com/gotalab/skillport/issues/60)) ([2969cd8](https://github.com/gotalab/skillport/commit/2969cd8fd4679c37ecbcf6cfdada59691bebb226))
* add validation rules for reserved words, XML tags, and type checks ([#54](https://github.com/gotalab/skillport/issues/54)) ([5e41fb2](https://github.com/gotalab/skillport/commit/5e41fb2b6302a672f16b81b0e0ca2da35485bffe))


### Bug Fixes

* expand tilde paths cross-platform ([#61](https://github.com/gotalab/skillport/issues/61)) ([b10ba48](https://github.com/gotalab/skillport/commit/b10ba48b11a7b04ffd571c3316835d84cc73a6f3))
* harden path handling for cross-platform security ([#57](https://github.com/gotalab/skillport/issues/57)) ([192d448](https://github.com/gotalab/skillport/commit/192d4483400d346b5dbd7ddd5767f00367d14e5c))
* support /blob/ format in GitHub URL parsing ([#58](https://github.com/gotalab/skillport/issues/58)) ([27cfe25](https://github.com/gotalab/skillport/commit/27cfe25c056e86f41c993be9022c09ab193e733d))


### Code Refactoring

* split CLI and MCP server into separate distributions ([#56](https://github.com/gotalab/skillport/issues/56)) ([bb03e3a](https://github.com/gotalab/skillport/commit/bb03e3a374b1c47e073f47704b222836613cf1fc))

## [0.6.1](https://github.com/gotalab/skillport/compare/v0.6.0...v0.6.1) (2025-12-21)


### Bug Fixes

* use Path.name for cross-platform directory extraction ([#52](https://github.com/gotalab/skillport/issues/52)) ([68b9f2f](https://github.com/gotalab/skillport/commit/68b9f2f9714d3209d950da511f323c3fc386d65a))

## [0.6.0](https://github.com/gotalab/skillport/compare/v0.5.2...v0.6.0) (2025-12-20)


### Features

* add GitHub shorthand format for add command ([#50](https://github.com/gotalab/skillport/issues/50)) ([4b0700d](https://github.com/gotalab/skillport/commit/4b0700d1ad0f22b8dbb361615cd99bdd7e9915a2))
* auto-detect GitHub auth via gh CLI ([#48](https://github.com/gotalab/skillport/issues/48)) ([758ac1f](https://github.com/gotalab/skillport/commit/758ac1f6ae442dd270805fef94ac9a7164cad119))

## [0.5.2](https://github.com/gotalab/skillport/compare/v0.5.1...v0.5.2) (2025-12-18)


### Bug Fixes

* align frontmatter validation with Agent Skills open standard ([#46](https://github.com/gotalab/skillport/issues/46)) ([0274cae](https://github.com/gotalab/skillport/commit/0274cae9aa1e760b66a1fa353a83816506781e22))

## [0.5.1](https://github.com/gotalab/skillport/compare/v0.5.0...v0.5.1) (2025-12-17)


### Bug Fixes

* upgrade lancedb to 0.26.0 and fix deprecation warnings ([#44](https://github.com/gotalab/skillport/issues/44)) ([52911ae](https://github.com/gotalab/skillport/commit/52911ae18531482fc763fca45e53ed7bfcf6e40e))

## [0.5.0](https://github.com/gotalab/skillport/compare/v0.4.1...v0.5.0) (2025-12-16)


### Features

* add location element and proper XML format for skill-client-integration spec compliance ([#42](https://github.com/gotalab/skillport/issues/42)) ([c052a45](https://github.com/gotalab/skillport/commit/c052a45f5419f2a4aec2c2c510c81606f3fdb317))

## [0.4.1](https://github.com/gotalab/skillport/compare/v0.4.0...v0.4.1) (2025-12-13)


### Bug Fixes

* **cli:** add Claude Code incompatibility warning for namespace option ([#40](https://github.com/gotalab/skillport/issues/40)) ([4951bdb](https://github.com/gotalab/skillport/commit/4951bdb72e466b010ecc5414e04ce71d144cd36a))

## [0.4.0](https://github.com/gotalab/skillport/compare/v0.3.1...v0.4.0) (2025-12-10)


### Features

* add zip file support for skill installation ([#37](https://github.com/gotalab/skillport/issues/37)) ([0b9fce4](https://github.com/gotalab/skillport/commit/0b9fce41cf315605c2aabc4ac8908948b7bafae2))

## [0.3.1](https://github.com/gotalab/skillport/compare/v0.3.0...v0.3.1) (2025-12-07)


### Bug Fixes

* use POSIX paths for cross-platform compatibility ([#35](https://github.com/gotalab/skillport/issues/35)) ([db7ad78](https://github.com/gotalab/skillport/commit/db7ad78cb878cbc51ca303a567f406a8b578b4fa))

## [0.3.0](https://github.com/gotalab/skillport/compare/v0.2.0...v0.3.0) (2025-12-07)


### Features

* show untracked skills in update command ([#31](https://github.com/gotalab/skillport/issues/31)) ([1e3a9dc](https://github.com/gotalab/skillport/commit/1e3a9dca8267eb14de804e951cad7fec2fa60098))
* show untracked skills in update command ([#34](https://github.com/gotalab/skillport/issues/34)) ([12873a1](https://github.com/gotalab/skillport/commit/12873a1c63805498ffa186c8d32cb74e7ca350a8))


### Reverts

* show untracked skills in update command ([6422fda](https://github.com/gotalab/skillport/commit/6422fdaa2326b003d0a7daa7264cc7a254d34f9b))

## [0.2.0](https://github.com/gotalab/skillport/compare/v0.1.6...v0.2.0) (2025-12-06)


### Features

* add Codex skills directory option to init command ([#29](https://github.com/gotalab/skillport/issues/29)) ([9d44f6e](https://github.com/gotalab/skillport/commit/9d44f6e0d5305936ba7d32a6b21d96e16f5772c0))
* add skill update command and configure ruff linting ([#26](https://github.com/gotalab/skillport/issues/26)) ([c6f0ab9](https://github.com/gotalab/skillport/commit/c6f0ab922c46216d51b1d9b730bf044f9863bd8a))


### Documentation

* add update command documentation and fix init example ([#30](https://github.com/gotalab/skillport/issues/30)) ([0c14b86](https://github.com/gotalab/skillport/commit/0c14b8695c4388c8f21ef7ff1d944d47ba5cbc4d))

## [0.1.6](https://github.com/gotalab/skillport/compare/v0.1.5...v0.1.6) (2025-12-05)


### Bug Fixes

* change cli command sync to doc ([a28d95c](https://github.com/gotalab/skillport/commit/a28d95c4440392c824e4e6daa145cbf4f2efa380))


### Documentation

* add Hugging Face Skills, remove SkillsMP Marketplace ([4f153cd](https://github.com/gotalab/skillport/commit/4f153cd0ac9c9582c6a81c30d0ab92b49fe0ca6c))
* add recommended community skills table to README ([913dc27](https://github.com/gotalab/skillport/commit/913dc27f498b8b1dc0d5dace2fb8311d977d2a2f))
* add recommended community skills table to README ([d40f04e](https://github.com/gotalab/skillport/commit/d40f04e5b6ef9f189fe93fceaf45e2b990f57748))
* update how to add codex skills ([4814997](https://github.com/gotalab/skillport/commit/4814997dbb2a2eedc711cc9412e4d5d24164fea2))

## [0.1.5](https://github.com/gotalab/skillport/compare/v0.1.4...v0.1.5) (2025-12-04)


### Bug Fixes

* change dir name ([5d75837](https://github.com/gotalab/skillport/commit/5d758376a1d5c5a721b63e02a807c5804927152e))
* enforce strict frontmatter validation on add ([56e36e1](https://github.com/gotalab/skillport/commit/56e36e1df02f23705cbf7e23d067b2b2de961c60))
* enforce strict frontmatter validation on add ([b56fee9](https://github.com/gotalab/skillport/commit/b56fee94daf4ef105ba1d2fa469102c9ada21ce3))


### Documentation

* translate guide to English and update CONTRIBUTING.md ([2387d25](https://github.com/gotalab/skillport/commit/2387d2506b52655d80b0270b29f76f11770563d2))
* translate guide to English and update CONTRIBUTING.md ([749c272](https://github.com/gotalab/skillport/commit/749c27260d14bceaaf086647294c8e38ecdef05a))

## [0.1.4](https://github.com/gotalab/skillport/compare/v0.1.3...v0.1.4) (2025-12-03)


### Features

* add skill-evaluator skill ([591ccbe](https://github.com/gotalab/skillport/commit/591ccbe803376e6f73f4be2a02bb104afceed1a3))
* **validation:** add frontmatter validation rules ([d97fda4](https://github.com/gotalab/skillport/commit/d97fda4802275519eef742e6515897543d693b65))
* **validation:** add frontmatter validation rules ([1ba8884](https://github.com/gotalab/skillport/commit/1ba8884ccc81bad6f622a6429a89e0870431ad2d))


### Documentation

* add README in .agent/skills/ ([0ae05b5](https://github.com/gotalab/skillport/commit/0ae05b5d9d501ed077911f468de2217833b773f5))
* add README in .agent/skills/ ([f2d5523](https://github.com/gotalab/skillport/commit/f2d55238c11021cb480a56a7c86964eeea0681e2))
* clarify CLI init/add flow ([495defa](https://github.com/gotalab/skillport/commit/495defa8a547c2173a585e8f17c9e2f4d21d5c4a))
* clarify CLI init/add flow ([0a4b887](https://github.com/gotalab/skillport/commit/0a4b88752bde7ce140bce4bd5874e8b1aff27918))
* clarify CLI init/add flow ([a0ff6b2](https://github.com/gotalab/skillport/commit/a0ff6b2b725b458e65f0ca50b80507423837e58c))


### Miscellaneous Chores

* prepare release ([2684deb](https://github.com/gotalab/skillport/commit/2684debe9b5bc4764afdd348e0d7e088a89e7c8f))

## [0.1.3](https://github.com/gotalab/skillport/compare/v0.1.2...v0.1.3) (2025-12-02)


### Bug Fixes

* use raw FTS scores and fix scalar index  ([24442a9](https://github.com/gotalab/skillport/commit/24442a96873148150c797ffc46f364e2e2073b8d))
* use raw FTS scores and fix scalar index type ([9e04d26](https://github.com/gotalab/skillport/commit/9e04d26366e3aab4e0c11f54a7caf145ccab77ff))

## [0.1.2](https://github.com/gotalab/skillport/compare/v0.1.1...v0.1.2) (2025-12-02)


### Bug Fixes

* auto reindex read commands ([230a729](https://github.com/gotalab/skillport/commit/230a729c56bb383bde4fa4c3f38b50a25bdcd323))

## [0.1.1](https://github.com/gotalab/skillport/compare/v0.1.0...v0.1.1) (2025-12-02)


### Features

* **cli:** add global skills/db overrides ([c6bd235](https://github.com/gotalab/skillport/commit/c6bd2352609202fa627b89f845a9ca0ca96fa087))
* **cli:** add global skills/db overrides ([a8d3c44](https://github.com/gotalab/skillport/commit/a8d3c44ccb5aa692156ec29b71060b97ae353883))
* derive db/meta per skills dir and improve add UX ([111889a](https://github.com/gotalab/skillport/commit/111889a386439225d8b9831ca06ed0e96283881b))
* initial release ([82cdaea](https://github.com/gotalab/skillport/commit/82cdaea69cfc22aa93307f94b0ef3be83131782b))


### Bug Fixes

* clean prefetched github temp dir after rename ([780cd5d](https://github.com/gotalab/skillport/commit/780cd5d5409bf1e09f0adfdb21152e7f516ff597))
* reuse fetched source and embedding defaults ([d250ea3](https://github.com/gotalab/skillport/commit/d250ea377676e8df4ae789b93b3db58d8963d658))


### Documentation

* align config sample to AGENTS+GEMINI ([eb900b6](https://github.com/gotalab/skillport/commit/eb900b663c7d69d6210cde0664597d092d236bad))
* mention Antigravity in other clients list ([99778c7](https://github.com/gotalab/skillport/commit/99778c78c68900575e7c93d67730d1e4feede01c))


### Miscellaneous Chores

* set release package name ([6e63e66](https://github.com/gotalab/skillport/commit/6e63e666427930dc62baac842ea61070a29ded6a))
