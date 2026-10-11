"""OCCID2 live semantic algebra and observation store."""
from pathlib import Path

from .definitions import load_definitions
from .runtime import (
    AmbiguousSemanticMatch, Axis, AxisValue, Binding, ChartType, Component, Coord, Datum,
    Equation, ExpressionType, IllegalSemanticCombination, OpenExpression,
    Product, Query, RelationFact, RelationType, SemanticRegistry, SemanticSolverLimit,
    SemanticValue, Store, SubjectRef, UID, sem, value_semantics,
)
from .wire import decode, encode


def new_registry() -> SemanticRegistry:
    return SemanticRegistry.load(Path(__file__).with_name("definitions.yaml"))


def new_store(*, registry: SemanticRegistry | None = None) -> Store:
    return Store(registry=registry)


__all__ = [
    "AmbiguousSemanticMatch", "Axis", "AxisValue", "Binding", "ChartType", "Component", "Coord", "Datum",
    "Equation", "ExpressionType", "IllegalSemanticCombination", "OpenExpression",
    "Product", "Query", "RelationFact", "RelationType", "SemanticRegistry", "SemanticSolverLimit",
    "SemanticValue", "Store", "SubjectRef", "UID", "sem", "value_semantics", "decode", "encode",
    "load_definitions", "new_registry", "new_store",
]
