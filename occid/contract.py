from __future__ import annotations

import argparse
import ast
import json
import shutil
import subprocess
import sys
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
        raise ContractError(f"missing checked-in OCCID contract marker: {path}")
    try:
        marker = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ContractError(f"invalid OCCID contract marker: {path}: {exc}") from exc
    if (
        not isinstance(marker, dict)
        or marker.get("format") != FORMAT_VERSION
        or not isinstance(marker.get("global_hash"), str)
    ):
        raise ContractError(f"invalid OCCID contract marker: {path}")
    return marker


def _build(repo_root: str | Path, *, include_modules: bool = True) -> dict[str, Any]:
    try:
        return build_manifest(repo_root, include_modules=include_modules)
    except SchemaContractError as exc:
        raise ContractError(str(exc)) from exc


def write_manifest(repo_root: str | Path, *, include_modules: bool = True) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    manifest = _build(root, include_modules=include_modules)
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
    manifest = _build(root)
    if _read_marker(root) != _marker(manifest):
        raise ContractError(
            f"checked-in {MANIFEST_NAME} is stale; run the OCCID generators before committing"
        )
    return manifest


def verify_manifest(repo_root: str | Path, *, include_modules: bool = True) -> None:
    root = Path(repo_root).resolve()
    manifest = _build(root, include_modules=include_modules)
    if _read_marker(root) != _marker(manifest):
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


def read_lock(source_root: str | Path) -> dict[str, Any]:
    path = lock_path(source_root)
    if not path.is_file():
        raise ContractError(
            f"missing OCCID consumer lock: {path}; run `python -m occid.contract lock {Path(source_root).resolve()}`"
        )
    try:
        lock = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ContractError(f"invalid OCCID consumer lock: {path}: {exc}") from exc
    if (
        not isinstance(lock, dict)
        or lock.get("format") != FORMAT_VERSION
        or not isinstance(lock.get("global_hash"), str)
        or not isinstance(lock.get("symbols"), dict)
    ):
        raise ContractError(f"invalid OCCID consumer lock: {path}")
    return lock


def write_lock(source_root: str | Path, occid_root: str | Path | None = None) -> dict[str, Any]:
    current = load_manifest(occid_root)
    used = sorted(scan_used_symbols(source_root, current))
    lock = {
        "format": FORMAT_VERSION,
        "global_hash": current["global_hash"],
        "symbols": {name: current["symbols"][name]["hash"] for name in used},
    }
    lock_path(source_root).write_text(
        json.dumps(lock, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return lock


def check_consumer(source_root: str | Path, occid_root: str | Path | None = None) -> ContractCheck:
    current = load_manifest(occid_root)
    lock = read_lock(source_root)
    baseline_hash = str(lock["global_hash"])
    expected = {str(name): str(value) for name, value in lock["symbols"].items()}

    scan_manifest = {"symbols": {name: {} for name in set(current["symbols"]) | set(expected)}}
    used = tuple(sorted(scan_used_symbols(source_root, scan_manifest)))

    if baseline_hash == current["global_hash"]:
        return ContractCheck(True, True, used, (), {}, baseline_hash, current["global_hash"])

    if not expected:
        raise ContractError(
            f"{lock_path(source_root)} only records an exact global baseline; validate the consumer against current OCCID and run `python -m occid.contract lock {Path(source_root).resolve()}`"
        )

    changed = [
        name
        for name in used
        if current["symbols"].get(name, {}).get("hash") != expected.get(name)
    ]
    causes = {name: (name,) for name in changed}
    return ContractCheck(
        not changed,
        False,
        used,
        tuple(changed),
        causes,
        baseline_hash,
        current["global_hash"],
    )


def assert_consumer(source_root: str | Path, occid_root: str | Path | None = None) -> ContractCheck:
    result = check_consumer(source_root, occid_root)
    if result.compatible:
        return result
    lines = [
        "OCCID contract mismatch:",
        f"  baseline global: {result.baseline_global_hash}",
        f"  current global:  {result.current_global_hash}",
    ]
    lines.extend(f"  {name}: changed" for name in result.changed_symbols)
    raise ContractError("\n".join(lines))


def model_hashes_for_ids(manifest: dict[str, Any], model_ids: Iterable[int]) -> dict[int, str]:
    wanted = {int(value) for value in model_ids}
    result: dict[int, str] = {}
    for entry in manifest["symbols"].values():
        model_id = entry.get("model_id")
        if model_id in wanted:
            result[int(model_id)] = str(entry["hash"])
    missing = sorted(wanted - set(result))
    if missing:
        raise ContractError(f"current OCCID does not define model IDs: {missing}")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="OCCID structural contract checks")
    sub = parser.add_subparsers(dest="command", required=True)
    default = str(Path(__file__).resolve().parents[1])
    for name in ("manifest", "verify"):
        p = sub.add_parser(name)
        p.add_argument("occid_root", nargs="?", default=default)
    for name in ("scan", "lock", "check"):
        p = sub.add_parser(name)
        p.add_argument("consumer_root")
        p.add_argument("--occid-root", default=default)
    args = parser.parse_args(argv)
    try:
        if args.command == "manifest":
            print(write_manifest(args.occid_root)["global_hash"])
        elif args.command == "verify":
            verify_manifest(args.occid_root)
            print("OCCID contract marker: current")
        elif args.command == "scan":
            print("\n".join(sorted(scan_used_symbols(args.consumer_root, load_manifest(args.occid_root)))))
        elif args.command == "lock":
            lock = write_lock(args.consumer_root, args.occid_root)
            print(lock["global_hash"])
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
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())