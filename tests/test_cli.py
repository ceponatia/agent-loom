from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agent_loom.cli import main


class CliTests(unittest.TestCase):
    def test_init_check_and_doctor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            self.assertEqual(main(["init", str(root), "--preset", "minimal", "--platform", "both"]), 0)
            self.assertEqual(main(["check", "--root", str(root)]), 0)
            self.assertIn(main(["doctor", "--root", str(root)]), {0, 1})

    def test_init_refuses_existing_agents(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".agents").mkdir()
            self.assertEqual(main(["init", str(root)]), 2)

    def test_init_rolls_back_generated_state_when_root_guidance_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            (root / "AGENTS.md").write_text(
                "<!-- agent-loom:start -->\nexisting\n<!-- agent-loom:end -->\n", encoding="utf-8"
            )
            self.assertEqual(
                main(["init", str(root), "--preset", "minimal", "--platform", "both", "--install-root-guidance"]),
                2,
            )
            self.assertFalse((root / ".agents").exists())
            self.assertFalse((root / ".claude" / "agents").exists())
            self.assertFalse((root / ".codex" / "agents").exists())


if __name__ == "__main__":
    unittest.main()
