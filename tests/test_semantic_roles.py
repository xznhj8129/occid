from __future__ import annotations

from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = REPO_ROOT / "lib" / "schema"
VALID_ROLES = {"concept", "representation"}


def _authored_models() -> dict[str, dict]:
    models: dict[str, dict] = {}
    for path in sorted(SCHEMA_ROOT.rglob("*.schema.yaml")):
        document = yaml.safe_load(path.read_text()) or {}
        for model_name, spec in (document.get("models") or {}).items():
            assert model_name not in models
            models[model_name] = spec
    return models


def test_every_model_has_explicit_semantic_role() -> None:
    for path in sorted(SCHEMA_ROOT.rglob("*.schema.yaml")):
        document = yaml.safe_load(path.read_text()) or {}
        for model_name, spec in (document.get("models") or {}).items():
            role = spec.get("semantic_role")
            assert role in VALID_ROLES, f"{path}: {model_name} missing/invalid semantic_role"
            if role == "representation":
                assert spec.get("parent"), f"{path}: Representation {model_name} must declare parent"


def test_compiled_levels_match_authored_semantics() -> None:
    models = _authored_models()
    concept_children: dict[str, list[str]] = {}
    for model_name, spec in models.items():
        parent = spec.get("parent")
        if parent and spec.get("semantic_role") == "concept":
            concept_children.setdefault(parent, []).append(model_name)

    compiled = yaml.safe_load((REPO_ROOT / "occid.yaml").read_text())
    types = compiled["types"]
    representations = compiled["representations"]

    for model_name, spec in models.items():
        role = spec["semantic_role"]
        if role == "representation":
            assert model_name in representations
            assert model_name not in types
        elif concept_children.get(model_name):
            assert model_name not in types
            assert model_name not in representations
        else:
            assert model_name in types
            assert model_name not in representations

    for section in (types, representations):
        for spec in section.values():
            assert "parent" not in spec
            assert "variants" not in spec
            assert "semantic_role" not in spec
