# Agent-system maintenance

Canonical sources live under `.agents/`. Change `catalog.json`, `common.md`, `roles/`, or `skills/`, then run `agent-loom sync`. Never hand-edit generated files recorded in `.agents/generated-manifest.json`.

Run `agent-loom check` before committing changes to the agent system. Treat model aliases, tool availability, and sandbox behavior as runtime capabilities to verify rather than promises made by the generator.
