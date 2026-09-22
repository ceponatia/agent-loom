---
name: example-implement
description: "Implement a bounded code change against issue acceptance with exclusive write ownership and verified targeted checks. Not permission to widen architecture, push, or merge."
---

# Implement a bounded slice

Confirm the assigned worktree, actual base SHA, dependency commits, owned paths, and allowed commands. Read the existing contract and nearest tests. A wrong base or missing write isolation must be resolved before editing.

Implement the smallest coherent change, including regression protection. Exercise the behavior through verified commands; a generated test that never runs is not validation. Preserve existing tests unless evidence justifies a changed contract.

Keep each failed repair hypothesis tied to its original finding. Routine syntax correction and intentional red-first testing are not automatic premium escalations; repeated ineffective fixes and cross-boundary uncertainty are. Load `example-escalate` only when its conditions apply.

Inspect the final diff for scope drift, secrets, generator-output edits, and compatibility consequences. Commit only authorized explicit paths. Return patch/commit identity, changed behavior, commands/results, remaining acceptance, and blockers. Do not push or alter GitHub state as a coding worker.
