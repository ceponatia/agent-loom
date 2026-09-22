# Routing and budgets

These are proposed starting rules, not measured optimums. `catalog.json` is the executable generator input for native model/effort settings. `policy.json` is custom project policy, not a vendor-enforced configuration file. Changes to routing budgets require owner approval, not a worker's convenience.

## Routes

| Task | Default route | Add only when justified |
|---|---|---|
| Simple factual question | Main session or reader | No coding team |
| Bounded routine issue | Orchestrator → coder → reviewer → PR manager | Reader for unfamiliar code; docs if references change |
| Significant behavior change | Same, plus independent test-maintainer | Architect if a shared contract is touched |
| High-risk save/schema/concurrency boundary | Architect if decision unresolved; advanced coder directly | Focused independent tests and premium review |
| CI failure | PR manager → CI investigator → coordinator | Coder for code; environment repair for access/runner failure |
| Repeated failed repair | Stop/preserve → advanced coder | Deep-rescue only under explicit approval |
| Issue-writing request | Issue-filer | Reader when evidence is missing; no automatic implementation |

The coordinator is normally the original top-level session, not a nested manager. Do not route a request to another orchestrator that then launches a second team. Workers, PR manager, and CI investigator return requests to the one coordinator. Native platforms can support more nesting than this policy permits; the flat topology is a deliberate cost/ownership choice. [S01, S04]

## Initial model/effort matrix

| Role | Codex | Claude Code |
|---|---|---|
| Orchestrator | GPT-5.6 Terra / high | Sonnet 5 / high |
| Reader | GPT-5.6 Luna / low | Haiku 4.5 / effort omitted |
| General coder | GPT-5.6 Terra / medium | Sonnet 5 / medium |
| Test-maintainer | GPT-5.6 Terra / high | Sonnet 5 / high |
| Documentation updater | GPT-5.6 Terra / medium | Sonnet 5 / medium |
| Issue-filer | GPT-5.6 Terra / medium | Sonnet 5 / medium |
| PR manager | GPT-5.6 Terra / low | Sonnet 5 / low |
| Advanced coder | GPT-5.6 Sol / xhigh | Opus 5 / xhigh |
| Reviewer | GPT-5.6 Sol / high | Opus 5 / high |
| Architect | GPT-5.6 Sol / xhigh | Opus 5 / xhigh |
| CI investigator | GPT-5.6 Terra / medium | Sonnet 5 / medium |
| Optional deep-rescue | GPT-5.6 Sol / max | Fable 5.1 / max |

Role choices are recommendations, not vendor benchmarks. Current model IDs and supported controls are source-backed; account availability and effective settings remain untested. Haiku's effort field is deliberately absent. Effort labels are not equal token budgets across models. Explicit IDs avoid accidentally inheriting an expensive model; the runtime must still detect substitutions/caps. [S09–S14]

Use Opus/Sol directly for known high-risk work rather than paying for a predictable weak attempt. Do not default every architect task to Fable max. Fable 5.1 and GPT-6 Astra are candidates to benchmark on the hardest tasks; “newest” does not establish lowest total accepted-work cost. The optional max route is deliberately gated. [S13–S14]

## Budget signals

Normally permit three active children, no more than two code writers, and one writer per worktree. A reader, two coders, and a reviewer do not all need to run simultaneously. Set limits using native configuration where supported; supervise actual counts and quota consumption too.

Record two failed repair hypotheses for the same finding before advanced reassignment. One advanced intervention is the default automatic cap. Intentional failing regression tests are not failed repairs. A second review round triggers reassessment, not an automatic unlimited fix loop. Track finding identity across new agents and head commits.

A routine task with roughly 12 minutes without meaningful progress should trigger a status inspection, not an automatic kill. This is a configurable starter heuristic, not a productivity benchmark. Exclude active builds/tests, queued tools, user approvals, known rate limits, and repository indexing. Count diagnostic evidence, useful patches, and completed checks—not tool-call volume. Replace a worker only after acknowledged cancellation and quiescence.

Neither the native `maxTurns` nor the illustrative stall timer is a complete usage budget. Native turn accounting differs, and a paused Claude worker can be resumed. An external controller needs a per-issue total budget and must carry it across resumes. Establish quota/dollar ceilings from the actual account before unattended operation. Do not invent a cash conversion for subscription usage.

A resumed worker does not get a fresh unlimited budget merely by being resumed (`no_budget_reset_on_new_agent`, `continuation_fraction_of_base_maxturns` in `policy.json`). For a routine coder/reviewer, one bounded continuation of roughly a third of the base `maxTurns` is the default ceiling when the transcript shows real progress — worked example: `example-general-coder` at 48 base turns gets at most one +16-turn continuation, 64 total, before the task must transfer to `example-advanced-coder` rather than receive a second continuation. The continuation itself requires evidence (useful patches, narrowing diagnosis, passing checks), not merely that the cap was reached; a worker stuck on repeated failed hypotheses escalates immediately instead, following the same two-hypothesis rule above rather than being granted more turns to keep failing the same way.

## Context economy

Use small task packets with source pointers. Readers return targeted evidence; workers verify important sources rather than receiving a whole repository dump. Preload one short primary skill per Claude role. Other skills load only when needed. Do not attach full transcripts to every handoff; preserve logs by reference and summarize failed hypotheses. Keep accepted task state in GitHub and restart metadata in ignored runtime state, not new planning documents.

See `evaluation.md` for a measured promotion/demotion process and `SOURCES.md` for source identifiers.
