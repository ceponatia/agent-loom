#!/usr/bin/env python3
"""Backward-compatible source-tree entry point for RoleSync."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if SRC.is_dir():
    sys.path.insert(0, str(SRC))

from rolesync.cli import legacy_sync_main  # noqa: E402
from rolesync.core import MANIFEST, render, sync  # noqa: E402,F401


def main() -> int:
    return legacy_sync_main(ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
