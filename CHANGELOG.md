# Changelog

## 1.0.0 - 2026-09-22

- Promote to a stable 1.0.0 release; no functional changes from 1.0.0rc1 beyond the items below.
- Fix `--version`'s fallback (used when the package metadata isn't available, e.g. running from a source checkout) to read from the package's single `__version__` instead of a separately hardcoded string.
- Correct README install/release notes now that the package is published and Trusted Publishing is confirmed working end-to-end.

## 1.0.0rc1 - 2026-09-22

- Renamed the project from `agent-loom` to RoleSync (PyPI package `rolesync`, CLI command `rolesync`) because the `agent-loom` name was already taken on PyPI.
- Package RoleSync as an installable Python CLI with `init`, `sync`, `check`, and `doctor` commands.
- Add `minimal` and `github-workflow` project presets and per-project Claude/Codex platform selection.
- Harden generated-file ownership against path traversal, symlink escapes, and malformed manifests.
- Mirror binary skill resources byte-for-byte while rejecting common secret-file patterns and transient files.
- Add cross-process locking plus recoverable staged synchronization for interrupted writes.
- Add cross-platform CI, built-wheel smoke testing, and a PyPI Trusted Publishing workflow.
