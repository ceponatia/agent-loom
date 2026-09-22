---
name: example-test
description: "Create or maintain regression, contract, integration, and save-compatibility tests from observable requirements. Use for meaningful coverage or test-quality work, not coverage-number inflation."
---

# Establish behavior evidence

Map each relevant acceptance criterion to a test or explicitly human check. Use deterministic time/random fixtures where needed; cover failure and boundary behavior at the owning layer. Inspect existing conventions before creating another framework or fixture abstraction.

For a defect, demonstrate the new test fails on the defective behavior and passes with the repair where feasible. Do not confuse the expected red-first failure with a failed repair attempt. For refactors, preserve contract evidence rather than pinning incidental implementation structure.

Run focused tests and necessary integration/build checks using established entry points. Record exact commands, revision, and results; distinguish missing tools, baseline failures, and code regressions. Any deliberate quarantine or skipped acceptance needs an issue and applicable approval.

Do not let tests silently approve their own changed expectations or visual baselines. Return the protected behavior and remaining gaps, not just a green summary.
