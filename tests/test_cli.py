from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rolesync.cli import main


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
                "<!-- rolesync:start -->\nexisting\n<!-- rolesync:end -->\n", encoding="utf-8"
            )
            self.assertEqual(
                main(["init", str(root), "--preset", "minimal", "--platform", "both", "--install-root-guidance"]),
                2,
            )
            self.assertFalse((root / ".agents").exists())
            self.assertFalse((root / ".claude" / "agents").exists())
            self.assertFalse((root / ".codex" / "agents").exists())

    def test_init_preserves_preexisting_files_in_managed_dirs_on_rollback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            unrelated = root / ".claude" / "agents" / "custom-agent.md"
            unrelated.parent.mkdir(parents=True)
            unrelated.write_text("not mine\n", encoding="utf-8")
            (root / "AGENTS.md").write_text(
                "<!-- rolesync:start -->\nexisting\n<!-- rolesync:end -->\n", encoding="utf-8"
            )
            self.assertEqual(
                main(["init", str(root), "--preset", "minimal", "--platform", "both", "--install-root-guidance"]),
                2,
            )
            self.assertFalse((root / ".agents").exists())
            self.assertEqual(unrelated.read_text(encoding="utf-8"), "not mine\n")
            self.assertFalse((root / ".claude" / "agents" / "loom-coder.md").exists())

    def test_init_restores_first_guidance_file_when_second_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            (root / "CLAUDE.md").write_text(
                "<!-- rolesync:start -->\nexisting\n<!-- rolesync:end -->\n", encoding="utf-8"
            )
            self.assertEqual(
                main(["init", str(root), "--preset", "minimal", "--platform", "both", "--install-root-guidance"]),
                2,
            )
            self.assertFalse((root / ".agents").exists())
            self.assertFalse((root / "AGENTS.md").exists())
            self.assertEqual(
                (root / "CLAUDE.md").read_text(encoding="utf-8"),
                "<!-- rolesync:start -->\nexisting\n<!-- rolesync:end -->\n",
            )


if __name__ == "__main__":
    unittest.main()
