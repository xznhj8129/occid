from __future__ import annotations

from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = REPO_ROOT / "lib" / "schema"
VALID_ROLES = {"ontology", "specialization"}


def test_every_model_has_explicit_semantic_role() -> None:
    for path in sorted(SCHEMA_ROOT.rglob("*.schema.yaml")):
        document = yaml.safe_load(path.read_text())
        for model_name, spec in (document.get("models") or {}).items():
            role = spec.get("semantic_role")
            assert role in VALID_ROLES, f"{path}: {model_name} missing/invalid semantic_role"
            if role == "specialization":
                assert spec.get("parent"), f"{path}: specialization {model_name} must declare parent"
