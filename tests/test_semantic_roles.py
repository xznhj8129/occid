from __future__ import annotations

from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = REPO_ROOT / "lib" / "schema"
VALID_ROLES = {"concept", "type", "representation"}


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
            assert "children" not in spec, f"{path}: {model_name} must declare ancestry only through parent"


def test_compiled_levels_match_authored_semantics() -> None:
    models = _authored_models()
    compiled = yaml.safe_load((REPO_ROOT / "occid.yaml").read_text())
    types = compiled["types"]
    representations = compiled["representations"]

    for model_name, spec in models.items():
        role = spec["semantic_role"]
        if role == "representation":
            assert model_name in representations
            assert model_name not in types
        elif role == "type":
            assert model_name in types
            assert model_name not in representations
        else:
            assert model_name not in types
            assert model_name not in representations

    for section in (types, representations):
        for spec in section.values():
            assert "parent" not in spec
            assert "semantic_role" not in spec


def test_compiled_children_are_derived_from_parent_edges() -> None:
    authored = _authored_models()
    compiled = yaml.safe_load((REPO_ROOT / "occid.yaml").read_text())
    emitted = {**compiled["types"], **compiled["representations"]}

    authored_children: dict[str, list[str]] = {}
    for child_name, spec in authored.items():
        parent = spec.get("parent")
        if parent:
            authored_children.setdefault(parent, []).append(child_name)

    def expected_children(model_name: str) -> list[str]:
        result: list[str] = []

        def walk(parent_name: str) -> None:
            for child_name in authored_children.get(parent_name, []):
                if child_name in emitted:
                    result.append(child_name)
                else:
                    walk(child_name)

        walk(model_name)
        return result

    for model_name, spec in emitted.items():
        assert spec.get("children", []) == expected_children(model_name)
