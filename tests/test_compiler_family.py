from __future__ import annotations

import compile_occid
import generate_pydantic as idl


def _compiled_contract() -> dict[str, object]:
    modules = idl.load_modules(
        idl.SCHEMA_DIR,
        idl.MODULE_DIR,
        [],
        [],
        True,
    )
    return compile_occid.Compiler(modules).compile()


def test_compiled_contract_carries_ancestry_only_through_parent() -> None:
    compiled = _compiled_contract()
    assert set(compiled) == {"version", "type", "vocabulary", "models", "maps"}
    assert "representations" not in compiled
    assert "concepts" not in compiled
    for spec in compiled["models"].values():
        assert "family" not in spec


def test_parent_edges_are_semantic_not_source_package() -> None:
    compiled = _compiled_contract()
    models = compiled["models"]
    assert models["Vehicle"]["parent"] == "Machine"
    assert models["AirRobot"]["parent"] == "AirMachine"
    assert models["Drone"]["parent"] == "AirRobot"
    assert models["Person"]["parent"] == "Actor"
    assert models["Machine"]["parent"] == "Entity"
    assert models["Actor"]["parent"] == "Entity"
