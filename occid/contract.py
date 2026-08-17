from __future__ import annotations

import argparse
import ast
import io
import json
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .contract_schema import SchemaContractError, build_manifest

MANIFEST_NAME = "occid-contract.json"
LOCK_NAME = "OCCID_CONTRACT"
FORMAT_VERSION = 1
IGNORED_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", ".tox", ".mypy_cache", ".pytest_cache", "build", "dist"}


class ContractError(RuntimeError):
    pass


@dataclass(frozen=True)
class ContractCheck:
    compatible: bool
    global_match: bool
    used_symbols: tuple[str, ...]
    changed_symbols: tuple[str, ...]
    changed_dependencies: dict[str, tuple[str, ...]]
    baseline_global_hash: str
    current_global_hash: str


def manifest_path(root: str | Path) -> Path:
    return Path(root).resolve() / MANIFEST_NAME


def _marker(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "format": FORMAT_VERSION,
        "release": manifest.get("release"),
        "global_hash": manifest["global_hash"],
    }


def _read_marker(root: str | Path) -> dict[str, Any]:
    path = manifest_path(root)
    if not path.is_file():
        raise ContractError(f"missing checked-in OCCID contract manifest: {path}")
    try:
        marker = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ContractError(f"invalid OCCID contract manifest: {path}: {exc}") from exc
    if (
        not isinstance(marker, dict)
        or marker.get("format") != FORMAT_VERSION
        or not isinstance(marker.get("global_hash"), str)
    ):
        raise ContractError(f"invalid OCCID contract manifest: {path}")
    return marker


def write_manifest(repo_root: str | Path, *, include_modules: bool = True) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    try:
        manifest = build_manifest(root, include_modules=include_modules)
    except SchemaContractError as exc:
        raise ContractError(str(exc)) from exc
    manifest_path(root).write_text(
        json.dumps(_marker(manifest), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    legacy_shards = root / "occid-contract"
    if legacy_shards.exists():
        shutil.rmtree(legacy_shards)
    return manifest


def load_manifest(repo_root: str | Path | None = None) -> dict[str, Any]:
    root = Path(repo_root).resolve() if repo_root is not None else Path(__file__).resolve().parents[1]
    marker = _read_marker(root)
    try:
        manifest = build_manifest(root)
    except SchemaContractError as exc:
        raise ContractError(str(exc)) from exc
    if marker != _marker(manifest):
        raise ContractError(
            f"checked-in {MANIFEST_NAME} is stale; run the OCCID generators before committing"
        )
    return manifest


def verify_manifest(repo_root: str | Path, *, include_modules: bool = True) -> None:
    root = Path(repo_root).resolve()
    marker = _read_marker(root)
    try:
        manifest = build_manifest(root, include_modules=include_modules)
    except SchemaContractError as exc:
        raise ContractError(str(exc)) from exc
    if marker != _marker(manifest):
        raise ContractError(
            f"checked-in {MANIFEST_NAME} is stale; run the OCCID generators before committing"
        )


def _python_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.py"):
        if not any(part in IGNORED_DIRS for part in path.relative_to(root).parts):
            yield path


def scan_used_symbols(source_root: str | Path, manifest: dict[str, Any] | None = None) -> set[str]:
    root = Path(source_root).resolve()
    known = set((manifest or load_manifest())["symbols"])
    used: set[str] = set()
    for path in _python_files(root):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (SyntaxError, UnicodeDecodeError) as exc:
            raise ContractError(f"cannot scan {path}: {exc}") from exc
        modules: set[str] = set()
        direct: dict[str, str] = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "occid":
                        modules.add(alias.asname or "occid")
            elif isinstance(node, ast.ImportFrom):
                if node.module == "occid" or (node.module or "").startswith("occid.schema"):
                    for alias in node.names:
                        if alias.name != "*":
                            direct[alias.asname or alias.name] = alias.name
                            if alias.name in known:
                                used.add(alias.name)
                else:
                    for alias in node.names:
                        if alias.name == "occid":
                            modules.add(alias.asname or "occid")
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id in modules and node.attr in known:
                used.add(node.attr)
            elif isinstance(node, ast.Name) and direct.get(node.id) in known:
                used.add(direct[node.id])
    return used


def lock_path(source_root: str | Path) -> Path:
    return Path(source_root).resolve() / LOCK_NAME


def read_lock(source_root: str | Path) -> str:
    path = lock_path(source_root)
    if not path.is_file():
        raise ContractError(f"missing OCCID consumer lock: {path}; run `python -m occid.contract lock {Path(source_root).resolve()}`")
    value = path.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ContractError(f"invalid OCCID consumer lock: {path}")
    return value


def write_lock(source_root: str | Path, occid_root: str | Path | None = None) -> str:
    value = load_manifest(occid_root)["global_hash"]
    lock_path(source_root).write_text(value + "\n", encoding="utf-8")
    return value


def _git(root: Path, *args: str, check: bool = True, binary: bool = False) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=check,
        text=not binary,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _git_json(root: Path, commit: str, path: str) -> dict[str, Any] | None:
    shown = _git(root, "show", f"{commit}:{path}", check=False)
    if shown.returncode:
        return None
    try:
        data = json.loads(shown.stdout)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def _historical_manifest(root: Path, commit: str) -> dict[str, Any]:
    archive = _git(
        root,
        "archive",
        "--format=tar",
        commit,
        "lib/schema",
        "lib/model_ids.yaml",
        "VERSION",
        binary=True,
    )
    with tempfile.TemporaryDirectory() as tmp:
        historical_root = Path(tmp)
        with tarfile.open(fileobj=io.BytesIO(archive.stdout), mode="r:") as tar:
            base = historical_root.resolve()
            for member in tar.getmembers():
                target = (historical_root / member.name).resolve()
                if target != base and base not in target.parents:
                    raise ContractError(f"unsafe path in historical OCCID archive: {member.name}")
            tar.extractall(historical_root)
        try:
            return build_manifest(historical_root)
        except SchemaContractError as exc:
            raise ContractError(
                f"cannot reconstruct OCCID contract at {commit}: {exc}"
            ) from exc


def load_historical_manifest(repo_root: str | Path, global_hash: str) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    current = load_manifest(root)
    if current["global_hash"] == global_hash:
        return current
    if not (root / ".git").exists():
        raise ContractError(f"OCCID history is required to compare baseline {global_hash}, but {root} is not a git checkout")
    commits = _git(root, "log", "--format=%H", "--all", "--", MANIFEST_NAME).stdout.splitlines()
    for commit in commits:
        marker = _git_json(root, commit, MANIFEST_NAME)
        if not marker or marker.get("global_hash") != global_hash:
            continue
        manifest = _historical_manifest(root, commit)
        if manifest["global_hash"] != global_hash:
            raise ContractError(
                f"historical OCCID contract marker at {commit} does not match its schema"
            )
        return manifest
    raise ContractError(f"OCCID baseline {global_hash} is not present in checked-in contract history")


def _closure(manifest: dict[str, Any], root_name: str) -> set[str]:
    symbols, seen, stack = manifest["symbols"], set(), [root_name]
    while stack:
        name = stack.pop()
        if name in seen or name not in symbols:
            continue
        seen.add(name)
        stack.extend(symbols[name].get("dependencies") or [])
    return seen


def compare_symbols(baseline: dict[str, Any], current: dict[str, Any], used_symbols: Iterable[str]) -> tuple[list[str], dict[str, tuple[str, ...]]]:
    old, new = baseline["symbols"], current["symbols"]
    changed: list[str] = []
    causes: dict[str, tuple[str, ...]] = {}
    for name in sorted(set(used_symbols)):
        if name in old and name in new and old[name].get("hash") == new[name].get("hash"):
            continue
        changed.append(name)
        if name not in old or name not in new:
            causes[name] = (name,)
            continue
        closure = _closure(baseline, name) | _closure(current, name)
        causes[name] = tuple(dep for dep in sorted(closure) if old.get(dep, {}).get("hash") != new.get(dep, {}).get("hash"))
    return changed, causes


def check_consumer(source_root: str | Path, occid_root: str | Path | None = None) -> ContractCheck:
    current = load_manifest(occid_root)
    baseline_hash = read_lock(source_root)
    if baseline_hash == current["global_hash"]:
        used = tuple(sorted(scan_used_symbols(source_root, current)))
        return ContractCheck(True, True, used, (), {}, baseline_hash, current["global_hash"])
    root = Path(occid_root).resolve() if occid_root is not None else Path(__file__).resolve().parents[1]
    baseline = load_historical_manifest(root, baseline_hash)
    scan_manifest = {"symbols": {**baseline["symbols"], **current["symbols"]}}
    used = tuple(sorted(scan_used_symbols(source_root, scan_manifest)))
    changed, causes = compare_symbols(baseline, current, used)
    return ContractCheck(not changed, False, used, tuple(changed), causes, baseline_hash, current["global_hash"])


def assert_consumer(source_root: str | Path, occid_root: str | Path | None = None) -> ContractCheck:
    result = check_consumer(source_root, occid_root)
    if result.compatible:
        return result
    lines = ["OCCID contract mismatch:", f"  baseline global: {result.baseline_global_hash}", f"  current global:  {result.current_global_hash}"]
    for name in result.changed_symbols:
        lines.append(f"  {name}: changed ({', '.join(result.changed_dependencies.get(name, ())) or name})")
    raise ContractError("\n".join(lines))


def model_symbols_for_ids(manifest: dict[str, Any], model_ids: Iterable[int]) -> dict[int, str]:
    wanted = {int(value) for value in model_ids}
    return {int(entry["model_id"]): name for name, entry in manifest["symbols"].items() if entry.get("model_id") in wanted}


def check_model_ids_against_baseline(baseline_global_hash: str, model_ids: Iterable[int], occid_root: str | Path | None = None) -> ContractCheck:
    current = load_manifest(occid_root)
    ids = tuple(sorted({int(value) for value in model_ids}))
    names = model_symbols_for_ids(current, ids)
    missing = [value for value in ids if value not in names]
    if missing:
        raise ContractError(f"current OCCID does not define stored model IDs: {missing}")
    used = tuple(sorted(names.values()))
    if baseline_global_hash == current["global_hash"]:
        return ContractCheck(True, True, used, (), {}, baseline_global_hash, current["global_hash"])
    root = Path(occid_root).resolve() if occid_root is not None else Path(__file__).resolve().parents[1]
    changed, causes = compare_symbols(load_historical_manifest(root, baseline_global_hash), current, used)
    return ContractCheck(not changed, False, used, tuple(changed), causes, baseline_global_hash, current["global_hash"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="OCCID schema contract fingerprints and consumer checks")
    sub = parser.add_subparsers(dest="command", required=True)
    default = str(Path(__file__).resolve().parents[1])
    for name in ("manifest", "verify"):
        p = sub.add_parser(name); p.add_argument("occid_root", nargs="?", default=default)
    for name in ("scan", "lock", "check"):
        p = sub.add_parser(name); p.add_argument("consumer_root"); p.add_argument("--occid-root", default=default)
    args = parser.parse_args(argv)
    try:
        if args.command == "manifest":
            print(write_manifest(args.occid_root)["global_hash"])
        elif args.command == "verify":
            verify_manifest(args.occid_root); print("OCCID contract manifest: current")
        elif args.command == "scan":
            print("\n".join(sorted(scan_used_symbols(args.consumer_root, load_manifest(args.occid_root)))))
        elif args.command == "lock":
            print(write_lock(args.consumer_root, args.occid_root))
        else:
            result = check_consumer(args.consumer_root, args.occid_root)
            if result.global_match:
                print(f"OCCID contract: OK (global {result.current_global_hash})")
            elif result.compatible:
                print("OCCID contract: OK (global changed; used symbols unchanged)")
            else:
                for symbol in result.changed_symbols:
                    print(f"OCCID contract changed: {symbol}", file=sys.stderr)
                return 1
    except (ContractError, SchemaContractError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr); return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
