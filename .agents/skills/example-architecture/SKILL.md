---
name: example-architecture
description: "Prepare a bounded, evidence-based architecture decision for GitHub when an implementation changes or depends on an unresolved cross-cutting contract."
---

# Resolve an architecture boundary

Identify the required outcome, existing implementation, accepted constraints, and actual decision needed. Distinguish a technical fact to verify from an owner preference or architectural tradeoff. Use a capability issue for an unresolved tool claim rather than building a design on it.

Compare the smallest viable option and a few meaningful alternatives. Explain contract ownership, failure behavior, persistence/asset consequences, validation, cost/maintenance, and reversibility. Avoid speculative general-purpose abstractions.

Prepare content for the existing decision-issue template with a recommendation, consequences, and revisit trigger. Do not create a parallel ADR or imply your recommendation is accepted. Unrelated work can continue while an affected slice waits for an actual decision.
