---
name: example-orchestrate
description: "Coordinate an authorized GitHub implementation task using scoped native roles, bounded retries, independent review, and a PR handoff. Use proactively for issue implementation; not for simple questions."
---

# Orchestrate an issue

Read the issue, current repository state, `.agents/policy.json`, and `.agents/references/routing-and-budgets.md`. Confirm authority and material unknowns. Use `.agents/references/handoff-contract.md` for compact task packets and checkpoints.

Classify scope/risk; retrieve focused context only as needed. Resolve blocking contract choices through the architect. Ask the PR manager/integrator to prepare an issue branch; create an early draft only once a meaningful commit exists. Follow `.agents/references/git-pr-lifecycle.md`.

Assign one coder by default. Use separate worktrees for independent parallel slices and serialize shared assets/integration. Require exact base and owned paths in every packet. Test specialists and documentation workers are conditional, not mandatory stages.

Track evidence of progress. For repeated failed hypotheses, stop and preserve the worker before advanced reassignment. Do not interpret an active test, queue, approval, or tool outage as deficient reasoning. Keep retries across agent replacements in one finding ledger.

Hitting `maxTurns` is a circuit breaker, not the escalation decision itself; read the transcript's evidence before acting. Progress (patches, narrowing diagnosis, passing checks) earns one bounded continuation, roughly a third of the base budget, per `.agents/references/routing-and-budgets.md`. Being stuck (repeated failed hypotheses, rereading/re-editing the same code) earns immediate escalation to the advanced coder instead — do not let a confused worker consume a continuation it will not use productively.

A worker launch failing on environment (missing prerequisite, stale detection, unavailable tool) is a separate problem from a reasoning failure. Fix or request the prerequisite, retry the same role once (`infrastructure_retries` in `.agents/policy.json`), then continue normal routing through that role. Only after that retry also fails should direct implementation by the coordinator be considered, and it must be disclosed, not quietly substituted for delegation.

Require independent review of the integrated current head and appropriate tests. Hand the reviewer an exact checkout path and expected head SHA it can actually reach — a reviewer has no isolation of its own, so if a worker's commit only exists in an isolated worktree, integrate or check it out somewhere reachable first. PR/CI agents return fixes to you; they do not create nested teams. Route semantic fixes back to coders, then revalidate. Report completion only after actual merge/acceptance, otherwise report the exact waiting/blocker state. Files do not provide persistent monitoring; see `runtime-and-security.md`.
