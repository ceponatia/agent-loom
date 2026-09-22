# Evaluate total accepted-work cost

The initial routing table is a hypothesis. There are no completed repository benchmarks in this kit. Optimize the complete outcome, not the nominal rate of the first worker.

## Small calibration set

Use approximately 15–20 representative, accepted tasks once the repository has enough real work. Include a bounded feature, a regression, persistence/schema compatibility, a test-gap task, documentation update, duplicate issue detection, valid/invalid PR comments, stale-head CI, and an intentionally missing capability. Add a parallel integration case and a canceled worker with a recoverable patch.

Replay independent candidates from the same clean base and acceptance contract. Compare one worker plus targeted review against unnecessary multi-role fan-out. Do not compare runs where one model gets better context, different permissions, or an already-repaired checkout. Avoid judging models solely on tasks they just saw during iterative tuning.

Record actual runtime/version/model/effort, input/output/cached/reasoning usage where exposed, subscription usage where measurable, tool time, review work, retries, interventions, accepted behavior, and any later regression. Unknown billing data stays unknown.

## Outcome table

| Measure | Why it matters |
|---|---|
| First-pass acceptance | Reduces repeated context and repair loops |
| Total usage through accepted merge | Includes retrieval, implementation, review, and fixes |
| Human interventions | Captures an expensive form of rework |
| Escaped regression/unsafe action | Quality and trust cannot be traded for a cheap first patch |
| Useful progress and wall-clock time | Distinguishes model work from test/tool waiting |
| Reviewer precision | Prevents expensive fixes to invented problems |
| Context size and duplicate reads | Detects orchestration overhead |

An evaluation record should include the complete finding lifecycle, not a reset count for each new worker. Track usage by role so low-value fan-out is visible.

## Adjust one thing at a time

First improve packet quality and role boundaries. Then compare effort or model tiers on the same task class. Promote directly to advanced for classes with repeated general-coder failures; demote only when accuracy and first-pass completion remain stable. Consider cheap mechanical docs/issue variants only after evidence shows low rework. Reassess premium review depth on trivial nonbehavioral changes without removing material-risk checks.

Test Sol/Opus and a newer premium alternative on a few truly difficult tasks before changing the default architecture route. Maximum effort is a candidate, not a universal best practice. Re-run a small calibration set after model/CLI updates or meaningful architecture changes.

GitHub capability/evaluation issues hold actual results and accepted policy changes. Keep only enduring guidance here, not a duplicate progress tracker.
