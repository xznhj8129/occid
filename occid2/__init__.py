"""OCCID2 live semantic algebra and observation store."""
from pathlib import Path

from .definitions import load_definitions
from .runtime import (
    AmbiguousSemanticMatch, Axis, AxisValue, ChartType, Coord, Datum,
    Equation, ExpressionType, IllegalSemanticCombination, OpenExpression,
    Product, RelationFact, RelationType, SemanticRegistry, SemanticSolverLimit,
    Store, SubjectRef, UID, sem, value_semantics,
)
from .wire import decode, encode


def new_registry() -> SemanticRegistry:
    return SemanticRegistry.load(Path(__file__).with_name("definitions.yaml"))


def new_store(path: str | Path | None = None, *, registry: SemanticRegistry | None = None) -> Store:
    return Store(registry=registry, path=path)


__all__ = [
    "AmbiguousSemanticMatch", "Axis", "AxisValue", "ChartType", "Coord", "Datum",
    "Equation", "ExpressionType", "IllegalSemanticCombination", "OpenExpression",
    "Product", "RelationFact", "RelationType", "SemanticRegistry", "SemanticSolverLimit",
    "Store", "SubjectRef", "UID", "sem", "value_semantics", "decode", "encode",
    "load_definitions", "new_registry", "new_store",
]
