from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path
from typing import Any, Iterable

from .contract_schema import SchemaContractError, build_manifest

OCCID_MARKER = "occid-contract.json"
CONSUMER_MANIFEST = "OCCID_CONTRACT"
FORMAT_VERSION = 1
IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".tox",
    ".mypy_cache",
    ".pytest_cache",
    "build",
    "dist",
}


class ContractError(RuntimeError):
    pass


def _installed_occid_root() -> Path:
    """Return the root belonging to the OCCID module imported by this Python."""
    return Path(__file__).resolve().parents[1]


def _marker(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "format": FORMAT_VERSION,
        "release": manifest.get("release"),
        "global_hash": manifest["global_hash"],
    }


def _read_json(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file():
        raise ContractError(f"missing {label}: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ContractError(f"invalid {label}: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError(f"invalid {label}: {path}")
    return value


def _build(root: Path) -> dict[str, Any]:
    try:
        return build_manifest(root)
    except SchemaContractError as exc:
        raise ContractError(str(exc)) from exc


def write_occid_marker(repo_root: str | Path) -> dict[str, Any]:
    """Regenerate OCCID's own checked-in structural marker."""
    root = Path(repo_root).resolve()
    manifest = _build(root)
    (root / OCCID_MARKER).write_text(
        json.dumps(_marker(manifest), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def current_manifest() -> dict[str, Any]:
    """Return the contract of the OCCID module actually imported by this Python."""
    root = _installed_occid_root()
    manifest = _build(root)
    marker = _read_json(root / OCCID_MARKER, "installed OCCID contract marker")
    if marker != _marker(manifest):
        raise ContractError(
            f"installed OCCID contract marker is stale: {root / OCCID_MARKER}; "
            "regenerate OCCID before using it"
        )
    return manifest


def _python_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.py"):
        if not any(part in IGNORED_DIRS for part in path.relative_to(root).parts):
            yield path


def scan_used_symbols(
    source_root: str | Path,
    manifest: dict[str, Any] | None = None,
) -> set[str]:
    """Find OCCID schema symbols referenced by a Python source tree."""
    root = Path(source_root).resolve()
    current = manifest or current_manifest()
    known = set(current["symbols"])
    used: set[str] = set()

    for path in _python_files(root):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, UnicodeError, SyntaxError) as exc:
            raise ContractError(f"cannot scan {path}: {exc}") from exc

        occid_aliases: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "occid":
                        occid_aliases.add(alias.asname or "occid")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if module == "occid" or module.startswith("occid.schema"):
                    for alias in node.names:
                        if alias.name == "*":
                            used.update(known)
                        elif alias.name in known:
                            used.add(alias.name)
                else:
                    # Some consumers deliberately re-export the imported SDK as
                    # ``occid``. Follow that alias without knowing their layout.
                    for alias in node.names:
                        if alias.name == "occid":
                            occid_aliases.add(alias.asname or "occid")

        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Attribute)
                and isinstance(node.value, ast.Name)
                and node.value.id in occid_aliases
                and node.attr in known
            ):
                used.add(node.attr)

    return used


def consumer_manifest_path(source_root: str | Path) -> Path:
    return Path(source_root).resolve() / CONSUMER_MANIFEST


def _read_consumer_manifest(source_root: str | Path) -> dict[str, Any]:
    path = consumer_manifest_path(source_root)
    value = _read_json(path, "OCCID consumer manifest")
    if (
        value.get("format") != FORMAT_VERSION
        or not isinstance(value.get("global_hash"), str)
        or not isinstance(value.get("symbols"), dict)
        or not all(
            isinstance(name, str) and isinstance(hash_value, str)
            for name, hash_value in value["symbols"].items()
        )
    ):
        raise ContractError(f"invalid OCCID consumer manifest: {path}")
    return value


def generate_consumer_manifest(source_root: str | Path = ".") -> dict[str, Any]:
    """Write the current installed OCCID fingerprints used by a source tree."""
    current = current_manifest()
    used = sorted(scan_used_symbols(source_root, current))
    receipt = {
        "format": FORMAT_VERSION,
        "global_hash": current["global_hash"],
        "symbols": {
            name: current["symbols"][name]["hash"]
            for name in used
        },
    }
    consumer_manifest_path(source_root).write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return receipt


def changed_symbols(source_root: str | Path = ".") -> tuple[str, ...]:
    """Compare a saved consumer manifest with the OCCID module imported now."""
    expected = _read_consumer_manifest(source_root)
    current = current_manifest()

    if expected["global_hash"] == current["global_hash"]:
        return ()

    if not expected["symbols"]:
        path = consumer_manifest_path(source_root)
        raise ContractError(
            f"{path} has no model fingerprints; "
            f"run `python -m occid.contract generate {Path(source_root).resolve()}`"
        )

    changed = [
        name
        for name, expected_hash in expected["symbols"].items()
        if current["symbols"].get(name, {}).get("hash") != expected_hash
    ]
    return tuple(sorted(changed))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate or check a consumer against the installed OCCID module"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("generate", "check"):
        command = sub.add_parser(name)
        command.add_argument("consumer_root", nargs="?", default=".")

    args = parser.parse_args(argv)

    try:
        if args.command == "generate":
            generate_consumer_manifest(args.consumer_root)
            print(f"OCCID manifest: {consumer_manifest_path(args.consumer_root)}")
            return 0

        changed = changed_symbols(args.consumer_root)
        if not changed:
            print("OCCID contract: same")
            return 0

        print("OCCID contract: different", file=sys.stderr)
        for name in changed:
            print(f"  {name}", file=sys.stderr)
        return 1
    except ContractError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
