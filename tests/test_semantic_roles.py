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
            assert "children" not in spec, f"{path}: {model_name} must declare ancestry only through parent"


def test_compiled_models_preserve_authored_semantic_role() -> None:
    authored = _authored_models()
    compiled = yaml.safe_load((REPO_ROOT / "occid.yaml").read_text())
    models = compiled["models"]

    assert set(models) == set(authored)
    for model_name, authored_spec in authored.items():
        compiled_spec = models[model_name]
        assert compiled_spec["semantic_role"] == authored_spec["semantic_role"]
        assert "family" not in compiled_spec

    assert "concepts" not in compiled
    assert "representations" not in compiled

def test_compiled_parent_and_children_are_one_graph() -> None:
    authored = _authored_models()
    compiled = yaml.safe_load((REPO_ROOT / "occid.yaml").read_text())
    emitted = compiled["models"]

    authored_children: dict[str, list[str]] = {}
    for child_name, spec in authored.items():
        parent = spec.get("parent")
        if parent:
            authored_children.setdefault(parent, []).append(child_name)

    for model_name, authored_spec in authored.items():
        compiled_spec = emitted[model_name]
        assert compiled_spec.get("parent") == authored_spec.get("parent")
        assert set(compiled_spec.get("children", [])) == set(authored_children.get(model_name, []))


def test_authored_hierarchy_has_no_second_membership_graph() -> None:
    for path in sorted(SCHEMA_ROOT.rglob("*.schema.yaml")):
        document = yaml.safe_load(path.read_text()) or {}
        for model_name, spec in (document.get("models") or {}).items():
            assert "variants" not in spec, f"{path}: {model_name} must use parent only"
            assert "children" not in spec, f"{path}: {model_name} children are compiler-derived"
