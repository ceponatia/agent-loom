---
name: example-review
description: "Independently review an exact code revision and integrated diff against requirements, invariants, security, and tests. Use before final acceptance of behavior-changing code."
---

# Review the current head

Obtain the issue contract, exact base/head, complete relevant diff, context map, and test evidence. Use a fresh reviewer that did not author the implementation. Read surrounding code and tests; examine the integrated result, not only individual slice reports.

The coordinator's brief must state the exact checkout/worktree path, base branch, and expected head SHA — never leave the reviewer to discover its own location. If the implementation's commit lives only in a worker's isolated worktree, integrate or check it out somewhere the reviewer can actually reach before dispatching; a reviewer that cannot see the real head will waste its budget reconstructing state instead of reviewing it. The reviewer verifies the stated head against its actual checkout first. Where a command/shell tool is granted and genuinely sandboxed read-only, treat read-only git commands as inspection tools, not as something to avoid because it "cannot modify source" — that boundary is about writes, not visibility. Where no such tool is granted (the ordinary case on a native adapter without an enforced read-only sandbox), verify the head by reading the repository's own ref files directly, and rely on coordinator-supplied verification evidence rather than trying to reproduce it — a prose-only "don't write" restriction on an ungated shell tool is not a substitute for the tool grant itself being scoped correctly.

Resolving the head this way from files alone requires following the actual git layout, not just `.git/refs/heads/<branch>` — that path only exists for a plain (non-worktree) checkout. In a linked worktree, `<checkout>/.git` is a plain-text file, not a directory:
1. If `<checkout>/.git` is a file, read it and follow the `gitdir: <path>` it names to find the real per-worktree git directory; otherwise `<checkout>/.git` already is that directory.
2. Read `<gitdir>/HEAD` to learn the current ref name (e.g. `ref: refs/heads/<branch>`) or a detached SHA.
3. To resolve a ref name to a commit, look for a `commondir` file inside that same `<gitdir>`; if present, resolve the relative path it contains (relative to `<gitdir>`) to find the shared common git directory — otherwise `<gitdir>` itself is the common directory.
4. Look for the ref as a loose file at `<common-dir>/refs/heads/<branch-name>`. If it is absent, git has likely packed it: read `<common-dir>/packed-refs` (a plain-text file; each relevant line is `<sha> refs/heads/<branch-name>`) and find the matching line.
5. If any path in this chain is outside what you can actually read, that is an unresolved verification gap, not an automatic hard blocker: report it to the coordinator and ask them to either grant the needed read access or independently confirm the head themselves, rather than stopping work or silently assuming a head.

Prioritize demonstrated correctness risks, unmet acceptance, security boundaries, persistence, and regression coverage. Avoid a mandatory findings quota and unrelated style cleanup. Report stable finding ID, severity, location, scenario, evidence, and the acceptance condition for resolution.

Reconcile previous findings explicitly as fixed, still open, invalid with rationale, or owner-deferred. An owner deferral must not silently waive required acceptance. Every changed head needs current-head attestation; proportionately inspect changed areas and interactions rather than blindly repeating a whole expensive review.

Return reviewed SHA and limitations. Your report is not automatically a GitHub approval or status check; the runtime must represent any enforced review gate through an authorized, head-bound mechanism.
