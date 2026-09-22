# Agent-system maintenance

Canonical role content is in `roles/`; metadata and model routing are in `catalog.json`; canonical skills are in `skills/`. Change those sources, then run `python scripts/sync_agents.py` from this repository or `rolesync sync` when the package is installed. Never hand-edit generated native roles or mirrored Claude skills.

Run `python scripts/sync_agents.py --check`, `python -m unittest discover -s scripts/tests -v`, and `python -m unittest discover -s tests -v`. Before a release, build and install the wheel and exercise the CLI outside the source checkout. Preserve native-only controls in the generator/catalog rather than contaminating portable skill frontmatter. Model aliases, effort support, and tool permissions require runtime verification; syntax checks alone do not establish availability.

Keep role instructions short, trigger descriptions discriminative, and procedural detail in on-demand skills/references. Do not silently modify owner approval or budget policy while implementing unrelated work.
