# Runtime capability and security boundaries

## What this kit implements

Shared role sources, portable skills, native generated definitions, model/effort starting settings, concise project instructions, deterministic generation/drift checking, and a smoke-test/evaluation checklist. These files guide a live agent session. They do **not** implement a running scheduler, GitHub webhook service, model-budget meter, credential broker, automatic repair loop, or restart-safe merge controller.

Begin with one native runtime per run: Codex or Claude Code can use the same behavioral sources without cross-provider plumbing. The top-level session follows the orchestrator role from root instructions. Native descriptions/skills support selection without the user naming each worker. Verify actual delegation with a small task; prompt-based routing is not a deterministic queue. [S01–S07]

Do not replace a platform's whole default system prompt merely to save one instruction import. The default setup here keeps normal main-session behavior and asks it to adopt the orchestrator role. Claude's optional `--agent example-orchestrator` is a separate opt-in: current documentation says a custom main agent replaces the default system prompt, so its behavior needs its own smoke test. Do not assume native orchestrator files change the current session model automatically. [S04]

## Current native adapters

Codex uses standalone `.codex/agents/<name>.toml`; this kit uses `name`, `description`, `model`, `model_reasoning_effort`, `sandbox_mode`, and `developer_instructions`. Current documentation supports these fields and project `[agents]` concurrency settings. It does not make our policy JSON or Claude `maxTurns` a native Codex turn budget. Model settings in a custom agent can override spawn preferences: use a correctly pinned role for escalation and verify effective settings. [S01, S15]

Claude uses `.claude/agents/<name>.md` with YAML controls. This kit preserves native `tools`, `permissionMode`, `maxTurns`, `skills`, `effort` where supported, and worktree isolation for file-writing specialist roles. Omitted effort for Haiku is intentional. Only one compact skill is preloaded per role. The no-descendant policy is reflected by withholding the Agent tool from worker definitions; this is a deliberate topology, not a claim Claude cannot nest agents. [S04, S09]

Canonical skills use the shared `name`/`description` frontmatter and ordinary Markdown. Claude-specific fork/model/argument/command features should live in native adapters if introduced, not silently added to the portable core. `agents/openai.yaml` is optional skill metadata; it is not the Codex native-agent definition. The checked-in Claude skill mirror avoids OS-specific symlink setup and is validated byte-for-byte. [S02, S05, S08]

Root `CLAUDE.md` imports `AGENTS.md`. Add the same small import beside each future scoped AGENTS file where Claude must load that domain's instructions. Do not assume a root import automatically discovers all descendant AGENTS files. Codex startup scoping and Claude on-demand scoping differ; workers still inspect applicable instructions for touched paths. [S03, S06]

## When a supervisor becomes necessary

Use native tools while the coordinator session remains active. Durable monitoring across closed/restarted sessions, mixed Codex/Claude workers, guaranteed time/usage caps, and reliable cancel-and-reassign behavior require a real supervisor. Keep it small; do not write an entire agent framework before testing native routing.

A later supervisor needs adapters for: start/resume; effective model/effort discovery; stream status/usage/tool events; stop/interrupt; wait for completion; capture artifacts; and safe credential contexts. OpenAI's Codex App Server exposes structured thread/turn methods including model discovery and interruption. Claude's programmatic/headless interface offers structured/streaming output and SDK integration. These are integration primitives, not an already installed daemon. [S21–S22]

A minimal state machine is:

```text
CLAIMED → CONTEXT → DISPATCHED → IMPLEMENTING → INTEGRATING
             ↑           ↓             ↓
          BLOCKED   STOPPING → PRESERVED → ADVANCED
                                        ↓
                       VERIFYING → REVIEWING → WAITING_CI
                                        ↑          ↓
                                    FIX_REQUEST ← findings
                                                   ↓
                                        MERGE_ELIGIBLE → MERGED → CLEANED/RETAINED
```

Persist run/issue IDs, branch lifetime, exact base/head, active worker/process IDs, write leases, finding/retry ledger, authorized effects/budgets, review head, CI run IDs, and the last processed event. Local `.agent-runs/` state is ignored operational metadata; a GitHub issue/PR checkpoint is the durable human-facing bookmark. Requirements still live only in GitHub.

Handle duplicate/out-of-order events idempotently. Re-fetch GitHub truth before consequential actions. After cancellation, confirm worker and child-process cessation before releasing the write lease. On restart, reconcile orphaned processes/worktrees instead of starting a competing writer. Wait on events/timers outside the LLM; wake a model only when a decision is needed.

## Permissions are not prose

A read-only filesystem sandbox does not establish read-only remote GitHub/MCP access. Conversely, allowing Bash permits more than the prose role intends. Tool allowlists, native sandbox/approval settings, least-privilege credentials, trusted hooks, and server-side GitHub rules must implement actual boundaries. The supplied settings do not pretend a shell command blacklist is a security sandbox. [S04, S15]

Prefer distinct credential contexts: coders/tests get no GitHub mutation/merge credential; readers/reviewers get local or read-only evidence; issue-filer gets only needed issue rights; PR operations run through an authorized writer. Do not test untrusted PR code with merge/publishing secrets. Disable unnecessary write-capable MCP integrations for read roles in the actual runtime; inherited connector access must be inspected, not assumed safe.

Merge automation is off until smoke tests verify runtime behavior, permissions, required checks/reviews, head freshness, and branch retention. Once the owner approves a repository/risk policy, individual routine tasks can proceed under it without repeated permission questions. Exceptions, purchases, protected contract changes, and subjective acceptance still require their applicable authority.

Subscription access does not automatically authorize metered API keys or third-party credits. The model catalog and final result metadata must be inspected on the user's account. Missing model access is a reported blocker or an owner-approved remapping, never a silent premium substitution.
