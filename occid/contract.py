from __future__ import annotations

import argparse
import ast
import json
import sys
from importlib.metadata import PackageNotFoundError, version as distribution_version
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
    """Return the contract root belonging to the OCCID module imported by this Python."""
    package_root = Path(__file__).resolve().parent
    if (package_root / "lib" / "schema").is_dir():
        return package_root
    return package_root.parent


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
    """Regenerate OCCID's checked-in source and package structural markers."""
    root = Path(repo_root).resolve()
    manifest = _build(root)
    marker_text = json.dumps(_marker(manifest), indent=2, sort_keys=True) + "\n"
    (root / OCCID_MARKER).write_text(marker_text, encoding="utf-8")
    package_marker = root / "occid" / OCCID_MARKER
    if package_marker.parent.is_dir():
        package_marker.write_text(marker_text, encoding="utf-8")
    return manifest


def current_manifest() -> dict[str, Any]:
    """Return the contract of the OCCID module actually imported by this Python."""
    root = _installed_occid_root()
    manifest = _build(root)
    if manifest.get("release") is None:
        try:
            manifest["release"] = distribution_version("occid")
        except PackageNotFoundError:
            pass
    marker = _read_json(root / OCCID_MARKER, "installed OCCID contract marker")
    if marker != _marker(manifest):
        raise ContractError(
            f"installed OCCID contract marker is stale: {root / OCCID_MARKER}; "
            "regenerate OCCID before using it"
        )
    return manifest


def load_manifest() -> dict[str, Any]:
    """Return the current structural contract for the imported OCCID module."""
    return current_manifest()


def model_hashes_for_ids(
    manifest: dict[str, Any],
    model_ids: Iterable[int],
) -> dict[int, str]:
    """Return structural hashes for permanent OCCID model IDs."""
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


def _python_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.py"):
        if not any(part in IGNORED_DIRS for part in path.relative_to(root).parts):
            yield path


def _attribute_root(node: ast.AST) -> str | None:
    current = node
    while isinstance(current, ast.Attribute):
        current = current.value
    return current.id if isinstance(current, ast.Name) else None


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
                    elif alias.name.startswith("occid.schema"):
                        occid_aliases.add(alias.asname or "occid")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if module == "occid" or module.startswith("occid.schema"):
                    for alias in node.names:
                        if alias.name == "*":
                            used.update(known)
                        elif module == "occid" and alias.name == "schema":
                            occid_aliases.add(alias.asname or "schema")
                        elif alias.name in known:
                            used.add(alias.name)
                else:
                    for alias in node.names:
                        if alias.name == "occid":
                            occid_aliases.add(alias.asname or "occid")

        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Attribute)
                and _attribute_root(node) in occid_aliases
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
    """Compare a saved consumer manifest with the imported OCCID module."""
    expected = _read_consumer_manifest(source_root)
    current = current_manifest()
    saved = expected["symbols"]

    scan_manifest = {
        "symbols": {
            name: current["symbols"].get(name, {})
            for name in set(current["symbols"]) | set(saved)
        }
    }
    used = scan_used_symbols(source_root, scan_manifest)

    untracked = sorted(used - set(saved))
    if untracked:
        path = consumer_manifest_path(source_root)
        names = ", ".join(untracked)
        raise ContractError(
            f"{path} is stale; untracked OCCID symbols: {names}; "
            f"run `python -m occid.contract generate {Path(source_root).resolve()}`"
        )

    if expected["global_hash"] == current["global_hash"]:
        return ()

    if not saved and used:
        path = consumer_manifest_path(source_root)
        raise ContractError(
            f"{path} has no model fingerprints; "
            f"run `python -m occid.contract generate {Path(source_root).resolve()}`"
        )

    changed = [
        name
        for name in used
        if current["symbols"].get(name, {}).get("hash") != saved[name]
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
