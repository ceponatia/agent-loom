# Agent-system maintenance

Canonical role content is in `roles/`; metadata and model routing are in `catalog.json`; canonical skills are in `skills/`. Change those sources, then run `agent-loom sync`. Never hand-edit generated native roles or mirrored Claude skills.

Run `agent-loom check` after agent-system changes. Preserve native-only controls in the catalog rather than contaminating portable skill frontmatter. Model aliases, effort support, tool availability, sandbox behavior, and connector permissions require runtime verification; generated syntax alone does not establish availability or enforcement.

Keep role instructions short, trigger descriptions discriminative, and procedural detail in on-demand skills/references. Do not silently modify owner approval or budget policy while implementing unrelated work.
