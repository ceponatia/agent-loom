---
name: example-ci
description: "Diagnose a specific CI/check failure from exact run/head evidence and distinguish code regression from infrastructure, stale results, configuration, or flakiness."
---

# Diagnose a failing check

Read the current PR head, run/job identifiers, triggering event, relevant workflow, and earliest actionable log error. Separate primary failure from downstream cancellation and compare baseline behavior when evidence is available.

Classify the failure and return a precise next step with confirmation evidence. Code defects go to a scoped coder; workflow defects need an authorized task; missing credentials/permissions are environment blockers. Permit only the bounded infrastructure retry in policy, not repeated attempts to obtain a lucky green run.

Check whether draft/ready events, path filters, or queue events prevented a required job from reporting. An absent required status is not success. Never change protection or skip a real failure merely to complete the issue. Do not execute untrusted branch code with merge/publishing credentials.
