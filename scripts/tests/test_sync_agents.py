"""Local structural tests; these do not launch Codex, Claude, or GitHub."""
from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("sync_agents", ROOT / "scripts/sync_agents.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def frontmatter(text: str) -> dict:
    """Parse the generator's restricted JSON-value YAML, not arbitrary YAML."""
    header = text.split("---\n", 2)[1]
    return {k: json.loads(v) for k, v in (line.split(": ", 1) for line in header.splitlines() if line.strip())}


class GenerationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / ".agents", self.root / ".agents")
        MODULE.sync(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def catalog(self):
        return json.loads((self.root / ".agents/catalog.json").read_text())

    def save_catalog(self, catalog):
        (self.root / ".agents/catalog.json").write_text(json.dumps(catalog))

    def test_clean_generation_and_idempotence(self):
        self.assertEqual(MODULE.sync(self.root, check=True), [])
        before = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        MODULE.sync(self.root)
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_all_roles_have_complete_native_adapters(self):
        common = (self.root / '.agents/common.md').read_text().strip()
        for r in self.catalog()['roles']:
            cx = tomllib.loads((self.root / '.codex/agents' / (r['name']+'.toml')).read_text())
            cltext = (self.root / '.claude/agents' / (r['name']+'.md')).read_text()
            cl = frontmatter(cltext)
            self.assertEqual(cx['name'], cl['name'])
            self.assertEqual(cx['model'], r['codex']['model'])
            self.assertEqual(cl['model'], r['claude']['model'])
            source = (self.root / r['source']).read_text().strip()
            self.assertIn(source, cx['developer_instructions'])
            self.assertIn(source, cltext)
            self.assertIn(common, cx['developer_instructions'])
            self.assertIn(common, cltext)
            self.assertNotIn('maxTurns', cx)
            self.assertNotIn('isolation', cx)
            self.assertEqual(cl['skills'], [r['skill']])

    def test_output_manifest_paths_use_portable_separators(self):
        outputs = MODULE.render(self.root)
        self.assertTrue(all("\\" not in p for p in outputs))

    def test_crlf_does_not_block_legitimate_regeneration(self):
        path = self.root / '.claude/agents/example-reader.md'
        path.write_bytes(path.read_bytes().replace(b'\n', b'\r\n'))
        source = self.root / '.agents/roles/reader.md'
        source.write_text(source.read_text()+'\nA valid new source rule.\n')
        MODULE.sync(self.root)
        self.assertEqual(MODULE.sync(self.root, check=True), [])

    def test_skills_are_exact_mirrors(self):
        for src in (self.root / '.agents/skills').rglob('SKILL.md'):
            dst = self.root / '.claude/skills' / src.relative_to(self.root / '.agents/skills')
            self.assertEqual(src.read_bytes(), dst.read_bytes())

    def test_worker_toolsets_are_flat(self):
        for r in self.catalog()['roles']:
            cl = frontmatter((self.root / '.claude/agents' / (r['name']+'.md')).read_text())
            self.assertEqual('Agent' in cl['tools'], r['id'] == 'orchestrator')
            self.assertEqual(cl['permissionMode'], 'default')

    def test_haiku_has_no_unsupported_effort(self):
        cl = frontmatter((self.root / '.claude/agents/example-reader.md').read_text())
        self.assertNotIn('effort', cl)

    def test_writer_native_base_warning_is_present(self):
        for r in self.catalog()['roles']:
            text = (self.root / '.claude/agents' / (r['name']+'.md')).read_text()
            if r['claude']['isolation']:
                self.assertEqual(frontmatter(text)['isolation'], 'worktree')
                self.assertIn('default branch rather than the assigned base', text)

    def test_canonical_update_refreshes_both_platforms(self):
        path = self.root / '.agents/roles/reader.md'
        path.write_text(path.read_text()+'\nNew bounded instruction.\n')
        self.assertTrue(MODULE.sync(self.root, check=True))
        MODULE.sync(self.root)
        self.assertEqual(MODULE.sync(self.root, check=True), [])
        for suffix in ['.codex/agents/example-reader.toml', '.claude/agents/example-reader.md']:
            self.assertIn('New bounded instruction.', (self.root / suffix).read_text())

    def test_modified_native_output_is_not_overwritten(self):
        path = self.root / '.claude/agents/example-reader.md'
        path.write_text(path.read_text()+'\nUntracked change.\n')
        self.assertIn('.claude/agents/example-reader.md', MODULE.sync(self.root, check=True))
        with self.assertRaisesRegex(ValueError, 'Refusing to overwrite'):
            MODULE.sync(self.root)

    def test_untracked_conflicting_output_is_not_overwritten(self):
        (self.root / MODULE.MANIFEST).unlink()
        path = self.root / '.codex/agents/example-reader.toml'
        path.write_text('name = "unrelated"\n')
        with self.assertRaisesRegex(ValueError, 'Refusing to overwrite'):
            MODULE.sync(self.root)

    def test_removed_role_prunes_only_owned_outputs(self):
        catalog = self.catalog()
        catalog['roles'] = [r for r in catalog['roles'] if r['id'] != 'deep-rescue']
        self.save_catalog(catalog)
        unrelated = self.root / '.claude/agents/unrelated.md'
        unrelated.write_text('Unrelated user file.\n')
        MODULE.sync(self.root)
        self.assertFalse((self.root / '.codex/agents/example-deep-rescue.toml').exists())
        self.assertTrue(unrelated.exists())

    def test_edited_stale_output_is_preserved(self):
        path = self.root / '.claude/agents/example-deep-rescue.md'
        path.write_text(path.read_text()+'\nKeep this.\n')
        catalog = self.catalog()
        catalog['roles'] = [r for r in catalog['roles'] if r['id'] != 'deep-rescue']
        self.save_catalog(catalog)
        with self.assertRaisesRegex(ValueError, 'Refusing to remove'):
            MODULE.sync(self.root)
        self.assertTrue(path.exists())

    def test_duplicate_or_invalid_names_rejected(self):
        catalog = self.catalog()
        catalog['roles'][1]['name'] = catalog['roles'][0]['name']
        self.save_catalog(catalog)
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            MODULE.sync(self.root)

    def test_role_source_path_escape_rejected(self):
        catalog = self.catalog()
        catalog['roles'][0]['source'] = '../outside.md'
        self.save_catalog(catalog)
        with self.assertRaisesRegex(ValueError, 'outside canonical'):
            MODULE.sync(self.root)

    def test_missing_skill_rejected(self):
        catalog = self.catalog()
        catalog['roles'][0]['skill'] = 'missing-skill'
        self.save_catalog(catalog)
        with self.assertRaisesRegex(ValueError, 'Missing skill'):
            MODULE.sync(self.root)

    def test_reviewer_security_boundary_is_pinned(self):
        """Security-boundary regression test.

        The reviewer must stay read-only on both platforms: Claude's tool
        grant must not silently regain unsandboxed shell (Bash) or the
        generic Skill tool (which would let it load unrelated skills at
        runtime), and Codex's sandbox_mode must not silently lose its
        enforced read-only sandbox. Exact-list/value equality is used
        deliberately, so an added tool, a reordering, or a loosened sandbox
        mode all fail this test immediately.
        """
        reviewer = next(r for r in self.catalog()['roles'] if r['id'] == 'reviewer')
        self.assertEqual(reviewer['claude']['tools'], ['Read', 'Grep', 'Glob'])
        self.assertEqual(reviewer['codex']['sandbox_mode'], 'read-only')

    def test_reviewer_generated_output_matches_security_boundary(self):
        """Confirm the generator faithfully mirrors the reviewer's catalog
        security boundary into the native outputs, so a generator bug
        cannot silently drift the rendered agent away from the pinned
        catalog source."""
        reviewer = next(r for r in self.catalog()['roles'] if r['id'] == 'reviewer')
        cl = frontmatter((self.root / '.claude/agents' / (reviewer['name']+'.md')).read_text())
        cx = tomllib.loads((self.root / '.codex/agents' / (reviewer['name']+'.toml')).read_text())
        self.assertEqual(cl['tools'], ['Read', 'Grep', 'Glob'])
        self.assertEqual(cx['sandbox_mode'], 'read-only')

    def test_committed_reviewer_output_matches_security_boundary(self):
        """Security-boundary regression test on the actually-committed
        files (not the temp-generated copy under self.root). A hand-edit
        directly to the checked-in .claude/agents/example-reviewer.md or
        .codex/agents/example-reviewer.toml that bypasses the generator (e.g.
        silently re-adding Bash or Skill) would not be caught by the
        temp-root tests above; only `sync_agents.py --check` catches that,
        and nothing runs it automatically. This test closes that gap."""
        cl = frontmatter((ROOT / '.claude/agents/example-reviewer.md').read_text())
        cx = tomllib.loads((ROOT / '.codex/agents/example-reviewer.toml').read_text())
        self.assertEqual(cl['tools'], ['Read', 'Grep', 'Glob'])
        self.assertEqual(cx['sandbox_mode'], 'read-only')


if __name__ == '__main__':
    unittest.main()
