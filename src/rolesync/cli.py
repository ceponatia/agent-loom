from __future__ import annotations

import argparse
import json
import shutil
import sys
from importlib import metadata, resources
from pathlib import Path

from .core import RoleSyncError, CONFIG, render, sync, validate_project


def version() -> str:
    try:
        return metadata.version("rolesync")
    except metadata.PackageNotFoundError:
        return "1.0.0rc1"


def _preset_root(name: str):
    base = resources.files("rolesync").joinpath("presets", name)
    if not base.is_dir():
        raise RoleSyncError(f"Unknown preset: {name}")
    return base


def _copy_resource_tree(source, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for child in source.iterdir():
        target = destination / child.name
        if child.is_dir():
            _copy_resource_tree(child, target)
        else:
            if target.exists():
                raise RoleSyncError(f"Refusing to overwrite existing file during init: {target}")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(child.read_bytes())


def _append_managed_block(path: Path, body: str) -> bool:
    start = "<!-- rolesync:start -->"
    end = "<!-- rolesync:end -->"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        if start in text or end in text:
            raise RoleSyncError(f"{path.name} already contains a rolesync managed block")
        prefix = text.rstrip() + "\n\n" if text.strip() else ""
    else:
        prefix = ""
    path.write_text(prefix + start + "\n" + body.rstrip() + "\n" + end + "\n", encoding="utf-8", newline="\n")
    return True


def _prune_empty_subdirs(path: Path) -> None:
    if not path.is_dir():
        return
    for child in sorted(path.iterdir()):
        if child.is_dir():
            _prune_empty_subdirs(child)
            try:
                child.rmdir()
            except OSError:
                pass


def init_project(root: Path, preset: str, platform: str, install_root_guidance: bool = False) -> None:
    root = root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    agents = root / ".agents"
    if agents.exists():
        raise RoleSyncError(f"Refusing to initialize over existing {agents}; adopt it manually or run sync/check instead")
    source = _preset_root(preset)
    managed_dirs = (root / ".codex" / "agents", root / ".claude" / "agents", root / ".claude" / "skills")
    preexisting_dirs = {d for d in managed_dirs if d.exists()}
    output_paths: list[Path] = []
    preexisting_outputs: set[Path] = set()
    guidance_writes: list[tuple[Path, bytes | None]] = []
    try:
        _copy_resource_tree(source, agents)
        platforms = ["claude", "codex"] if platform == "both" else [platform]
        (root / CONFIG).write_text(
            json.dumps({"schema_version": 1, "preset": preset, "platforms": platforms}, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        output_paths = [root / rel for rel in render(root)]
        preexisting_outputs = {p for p in output_paths if p.exists()}
        sync(root)
        if install_root_guidance:
            guidance = [(
                root / "AGENTS.md",
                "Agent definitions are maintained under `.agents/`. Follow `.agents/AGENTS.md` for agent-system maintenance. Do not hand-edit generated files under `.claude/agents/`, `.claude/skills/`, or `.codex/agents/`.",
            )]
            if "claude" in platforms:
                guidance.append((root / "CLAUDE.md", "@AGENTS.md"))
            for path, body in guidance:
                original = path.read_bytes() if path.exists() else None
                _append_managed_block(path, body)
                guidance_writes.append((path, original))
    except BaseException:
        for path, original in guidance_writes:
            if original is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(original)
        if agents.exists():
            shutil.rmtree(agents, ignore_errors=True)
        for path in output_paths:
            if path not in preexisting_outputs and path.exists():
                path.unlink(missing_ok=True)
        for managed_dir in managed_dirs:
            if managed_dir.exists():
                _prune_empty_subdirs(managed_dir)
                if managed_dir not in preexisting_dirs:
                    try:
                        managed_dir.rmdir()
                    except OSError:
                        pass
        raise


def _sync_command(root: Path, check: bool) -> int:
    try:
        problems = sync(root, check=check)
    except (OSError, UnicodeError, RoleSyncError, KeyError, TypeError) as exc:
        print(f"rolesync: {exc}", file=sys.stderr)
        return 2
    if check and problems:
        print("Generated files differ:", file=sys.stderr)
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1
    print("Generated files are current." if check else "Native agent files and mirrored skills generated.")
    return 0


def _doctor(root: Path) -> int:
    root = root.resolve()
    issues = validate_project(root)
    if issues:
        print(f"Project: {root}")
        for issue in issues:
            print(f"ERROR: {issue}")
        return 1
    drift = sync(root, check=True)
    config_path = root / CONFIG
    platforms = ["claude", "codex"]
    if config_path.is_file():
        config = json.loads(config_path.read_text(encoding="utf-8"))
        platforms = config.get("platforms", platforms)
    print(f"Project: {root}")
    print("Configuration: valid")
    print("Generated output: " + ("current" if not drift else "drifted"))
    for platform in platforms:
        executable = "claude" if platform == "claude" else "codex"
        found = shutil.which(executable)
        print(f"{platform}: {'found at ' + found if found else 'CLI not found on PATH (generation still works)'}")
    if drift:
        print("Drift:")
        for item in drift:
            print(f"  {item}")
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rolesync", description="Generate native Claude Code and Codex agent definitions from one canonical catalog.")
    parser.add_argument("--version", action="version", version=f"rolesync {version()}")
    sub = parser.add_subparsers(dest="command")

    init = sub.add_parser("init", help="Initialize a project from a built-in preset")
    init.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    init.add_argument("--preset", choices=["minimal", "github-workflow"], default="minimal")
    init.add_argument("--platform", choices=["both", "claude", "codex"], default="both")
    init.add_argument("--install-root-guidance", action="store_true", help="Append a small managed guidance block to root AGENTS.md and CLAUDE.md")

    for name, help_text in (("sync", "Validate and render native agent files"), ("check", "Report drift without writing"), ("doctor", "Validate setup and local runtime availability")):
        cmd = sub.add_parser(name, help=help_text)
        cmd.add_argument("--root", type=Path, default=Path.cwd())
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 0
    try:
        if args.command == "init":
            init_project(args.root, args.preset, args.platform, args.install_root_guidance)
            print(f"Initialized rolesync in {args.root.resolve()}")
            return 0
        if args.command == "sync":
            return _sync_command(args.root, check=False)
        if args.command == "check":
            return _sync_command(args.root, check=True)
        if args.command == "doctor":
            return _doctor(args.root)
    except (OSError, UnicodeError, RoleSyncError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"rolesync: {exc}", file=sys.stderr)
        return 2
    return 2


def legacy_sync_main(default_root: Path) -> int:
    parser = argparse.ArgumentParser(description="Render native Codex/Claude agents and mirror portable skills.")
    parser.add_argument("--root", type=Path, default=default_root)
    parser.add_argument("--check", action="store_true", help="Report missing/stale/drifted outputs without writing")
    args = parser.parse_args()
    return _sync_command(args.root, check=args.check)
