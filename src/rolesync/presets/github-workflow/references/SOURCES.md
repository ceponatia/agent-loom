# Sources and verification record

Research date: **2026-09-18**. Public primary documentation was inspected. Live Codex/Claude execution, account access, cost measurements, and GitHub automation were **not** tested. Models, capabilities, pricing, and CLI schemas can change; runtime verification is an installation requirement.

The kit's architecture, role split, thresholds, permissions proposal, and model routing are recommendations. The sources below support platform facts, not proof that this system is empirically optimal.

| ID | Primary source | Facts used |
|---|---|---|
| S01 | `https://developers.openai.com/codex/multi-agent` (redirects to ChatGPT Learn subagents) | Standalone TOML roles, native delegation, model/config inheritance, concurrency |
| S02 | `https://developers.openai.com/codex/skills` | Skill discovery, progressive loading, portable skill core, optional metadata |
| S03 | `https://developers.openai.com/codex/guides/agents-md` | AGENTS scope/discovery and precedence |
| S04 | `https://code.claude.com/docs/en/sub-agents` | Native role fields, effort, skills preload, tools, turns, isolation, model substitution, main-agent behavior |
| S05 | `https://code.claude.com/docs/en/skills` | Claude skill loading, platform-specific features |
| S06 | `https://code.claude.com/docs/en/memory` | CLAUDE.md imports and scoped instruction behavior |
| S07 | `https://code.claude.com/docs/en/best-practices` | Concise instructions, verification, context and correction discipline |
| S08 | `https://agentskills.io/specification` | Shared Agent Skills format |
| S09 | `https://platform.claude.com/docs/en/models/overview` | Current Claude model IDs, capabilities, default effort, API pricing |
| S10 | `https://code.claude.com/docs/en/model-config` | Current Claude Code model/effort configuration and availability caveats |
| S11 | `https://developers.openai.com/api/docs/models/gpt-5.6-luna` | Luna model and effort options |
| S12 | `https://developers.openai.com/api/docs/models/gpt-5.6-terra` | Terra model and effort options |
| S13 | `https://developers.openai.com/api/docs/models/gpt-5.6-sol` | Sol model and effort options |
| S14 | `https://developers.openai.com/api/docs/models/gpt-6-astra` | Higher-tier model to evaluate rather than assume as default |
| S15 | `https://developers.openai.com/codex/config-reference` | Supported session configuration, instructions vs prompt replacement, sandbox/connector distinctions |
| S16 | `https://docs.github.com/en/get-started/using-github/github-flow` | Branch/review/merge workflow |
| S17 | `https://docs.github.com/en/pull-requests/reference/pull-requests` | Draft PR behavior |
| S18 | `https://cli.github.com/manual/gh_pr_merge` | Head-match, auto-merge, deletion, and bypass flags |
| S19 | `https://git-scm.com/docs/git-worktree` | Separate worktree/branch mechanics |
| S20 | `https://docs.github.com/actions/using-workflows/events-that-trigger-workflows` | PR events, readiness, merge queue and token-trigger behavior |
| S21 | `https://developers.openai.com/codex/app-server` | Structured runtime methods, model discovery, turn interruption/events |
| S22 | `https://code.claude.com/docs/en/headless` | Structured programmatic runs and stream output |

## Validating against a real project (example only)

Before adopting this catalog, read a comparable project's own native agent definitions (`.claude/agents/*.md`, `.codex/agents/*.toml`) and any shared skill sources, if one is available for reference. Compare scoped briefs, path ownership, preserved escalation records, acceptance evidence, and the split between implementation and PR handling. Treat any patterns found this way as candidates to evaluate against this project's own constraints, not universal rules to import wholesale.

This kit's design was not validated by a full repository audit, hook-security assessment, runtime compatibility test, or efficiency benchmark of any specific project.
