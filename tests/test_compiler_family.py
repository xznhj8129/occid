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


def test_family_is_nearest_ancestor_concept() -> None:
    compiled = _compiled_contract()
    representations = compiled["representations"]
    assert isinstance(representations, dict)

    # Direct Representation -> Concept parent.
    assert representations["Vehicle"]["family"] == "Machine"

    # Representation chains do not become runtime ancestry. AirRobot and Drone
    # both walk through Representation parents until the nearest Concept.
    assert representations["AirRobot"]["family"] == "Machine"
    assert representations["Drone"]["family"] == "Machine"

    # A different branch retains only its own nearest Concept parent.
    assert representations["Person"]["family"] == "Actor"


def test_family_is_independent_of_source_package() -> None:
    compiled = _compiled_contract()
