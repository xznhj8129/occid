from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
from typing import Any, ClassVar, Iterable


@dataclass(frozen=True, slots=True)
class Product:
    terms: frozenset[str]

    def __mul__(self, other: Any) -> "Product":
        return self | sem(other)

    def __or__(self, other: "Product") -> "Product":
        return Product(self.terms | other.terms)

    def __contains__(self, term: Any) -> bool:
        return semantic_name(term) in self.terms

    def __iter__(self):
        return iter(sorted(self.terms))

    def __str__(self) -> str:
        return " × ".join(sorted(self.terms)) if self.terms else "∅"


EMPTY = Product(frozenset())


def product_names(names: Iterable[str]) -> Product:
    return Product(frozenset(names))


def semantic_name(term: Any) -> str:
    if isinstance(term, AxisValue):
        return term.name
    if isinstance(term, str):
        return term
    if isinstance(term, SemanticEnum):
        raise TypeError("surface enum values expand to products; use sem(value)")
    if isinstance(term, SemanticModelMeta):
        return term.__name__
    if hasattr(term, "_semantic_name"):
        return str(term._semantic_name)
    raise TypeError(f"not a semantic term: {term!r}")


def sem(*terms: Any) -> Product:
    out = EMPTY
    for term in terms:
        if term is None:
            continue
        if isinstance(term, Product):
            out = out | term
        elif isinstance(term, SemanticEnum):
            out = out | term._semantics
        elif isinstance(term, SemanticModelMeta):
            # In queries, a model class means the semantic region represented by
            # that class, not merely its spelling.
            out = out | term._semantics
        else:
            out = out | Product(frozenset({semantic_name(term)}))
    return out


class SemanticModelMeta(type):
    def __mul__(cls, other: Any) -> Product:
        return sem(cls) * other

    def __rmul__(cls, other: Any) -> Product:
        return sem(other) * cls


class SemanticModel(metaclass=SemanticModelMeta):
    _semantic_role: ClassVar[str] = "concept"
    _semantics: ClassVar[Product] = EMPTY


@dataclass(frozen=True, slots=True)
class AxisValue:
    axis: str
    value: str

    @property
    def name(self) -> str:
        return f"{self.axis}.{self.value}"

    def __mul__(self, other: Any) -> Product:
        return sem(self) * other

    def __rmul__(self, other: Any) -> Product:
        return sem(other) * self

    def __str__(self) -> str:
        return self.name


class SemanticAxis:
    _axis_name: ClassVar[str]
    _cardinality: ClassVar[str]
    _applies: ClassVar[Any] = None


class SemanticEnum(Enum):
    _semantic_map: ClassVar[dict[str, Product]]

    @property
    def _semantics(self) -> Product:
        return getattr(self.__class__, "_semantic_map", {}).get(self.name, EMPTY)


@dataclass(frozen=True, slots=True)
class RelationFact:
    relation: "RelationType"
    operands: tuple["ModelRef", ...]

    def __str__(self) -> str:
        return f"{self.relation.name}({', '.join(x.uid for x in self.operands)})"


@dataclass(frozen=True, slots=True)
class RelationType:
    name: str
    signature: tuple[type[SemanticModel], ...]

    def __call__(self, *operands: "ModelRef") -> RelationFact:
        if len(operands) != len(self.signature):
            raise TypeError(f"{self.name} expects {len(self.signature)} operands")
        for index, (operand, expected) in enumerate(zip(operands, self.signature)):
            if not issubclass(operand.model, expected):
                raise TypeError(
                    f"{self.name} operand {index} expects {expected.__name__}, "
                    f"got {operand.model.__name__}"
                )
        return RelationFact(self, tuple(operands))


@dataclass(slots=True)
class StoredDatum:
    subject_uid: str
    representation: type[SemanticModel]
    semantics: Product
    value: SemanticModel


class SemanticRegistry:
    def __init__(self, spec: dict[str, Any]):
        self.spec = spec
        self.axis_of_value: dict[str, str] = {}
        self.axis_cardinality: dict[str, str] = {}
        self.axis_applies: dict[str, Any] = {}
        for axis_name, axis in spec.get("axes", {}).items():
            self.axis_cardinality[axis_name] = axis.get("cardinality", "many")
            self.axis_applies[axis_name] = axis.get("applies")
            for value in axis.get("values", []):
                self.axis_of_value[f"{axis_name}.{value}"] = axis_name

    def closure(self, product: Product) -> Product:
        # For this bounded demo, applicability expressed as ALL(...) is also a
        # requirement of selecting a value on that axis. ANY(...) remains an
        # open completion constraint unless one alternative is already present.
        terms = set(product.terms)
        changed = True
        while changed:
            changed = False
            for term in list(terms):
                axis = self.axis_of_value.get(term)
                if not axis:
                    continue
                applies = self.axis_applies.get(axis)
                if isinstance(applies, dict) and "all" in applies:
                    for required in applies["all"]:
                        if required not in terms:
                            terms.add(required)
                            changed = True
                elif isinstance(applies, str) and applies not in terms:
                    terms.add(applies)
                    changed = True
        return product_names(terms)

    def legal(self, product: Product) -> bool:
        closed = self.closure(product)
        seen: dict[str, set[str]] = {}
        for term in closed.terms:
            axis = self.axis_of_value.get(term)
            if axis:
                seen.setdefault(axis, set()).add(term)
        for axis, values in seen.items():
            if self.axis_cardinality.get(axis) == "one" and len(values) > 1:
                return False
        return True

    def entails(self, product: Product, wanted: Any) -> bool:
        return self.closure(sem(wanted)).terms <= self.closure(product).terms

    def equivalent(self, left: Product, right: Product) -> bool:
        return self.closure(left).terms == self.closure(right).terms

    def applicable(self, product: Product, axis_or_value: Any) -> bool:
        if isinstance(axis_or_value, AxisValue):
            axis_name = axis_or_value.axis
        elif isinstance(axis_or_value, type) and issubclass(axis_or_value, SemanticAxis):
            axis_name = axis_or_value._axis_name
        else:
            axis_name = str(axis_or_value)
        applies = self.axis_applies.get(axis_name)
        if not applies:
            return True
        closed = self.closure(product).terms
        if isinstance(applies, str):
            return applies in closed
        if "all" in applies:
            return all(x in closed for x in applies["all"])
        if "any" in applies:
            return any(x in closed for x in applies["any"])
        return True


class AmbiguousSemanticMatch(LookupError):
    pass


class ModelRef:
    def __init__(self, store: "Store", uid: str, model: type[SemanticModel]):
        self.store = store
        self.uid = uid
        self.model = model

    @property
    def fields(self) -> tuple[str, ...]:
        if not is_dataclass(self.model):
            return ()
        return tuple(f.name for f in fields(self.model))

    @property
    def semantics(self) -> Product:
        return self.model._semantics | self.store._assertions.get(self.uid, EMPTY)

    def assert_(self, *terms: Any) -> "ModelRef":
        extra = sem(*terms)
        candidate = self.semantics | extra
        if not self.store.registry.legal(candidate):
            raise ValueError(f"illegal semantic assertion: {candidate}")
        self.store._assertions[self.uid] = self.store._assertions.get(self.uid, EMPTY) | extra
        return self

    def set(self, value: SemanticModel, *qualifiers: Any) -> SemanticModel:
        return self.store.set(self, value, *qualifiers)

    def get(self, *query: Any) -> SemanticModel:
        return self.store.get(self, *query)

    def find(self, *query: Any) -> list[SemanticModel]:
        return self.store.find(self, *query)

    def __repr__(self) -> str:
        return f"Ref[{self.model.__name__}]({self.uid!r})"


class Store:
    def __init__(self, registry: SemanticRegistry):
        self.registry = registry
        self._data: dict[str, list[StoredDatum]] = {}
        self._assertions: dict[str, Product] = {}
        self._relations: list[RelationFact] = []

    def ref(self, uid: str, model: type[SemanticModel]) -> ModelRef:
        return ModelRef(self, uid, model)

    def set(self, subject: ModelRef, value: SemanticModel, *qualifiers: Any) -> SemanticModel:
        rep = type(value)
        if getattr(rep, "_semantic_role", None) != "representation":
            raise TypeError(f"{rep.__name__} is not a representation")
        semantics = value_semantics(value) | sem(*qualifiers)
        if not self.registry.legal(semantics):
            raise ValueError(f"illegal datum semantics: {semantics}")
        bucket = self._data.setdefault(subject.uid, [])
        bucket[:] = [d for d in bucket if d.representation is not rep]
        bucket.append(StoredDatum(subject.uid, rep, semantics, value))
        return value

    def find(self, subject: ModelRef, *query: Any) -> list[SemanticModel]:
        wanted = sem(*query)
        out: list[SemanticModel] = []
        for datum in self._data.get(subject.uid, []):
            if self.registry.entails(datum.semantics, wanted):
                out.append(datum.value)
        return sorted(out, key=lambda x: type(x).__name__)

    def get(self, subject: ModelRef, *query: Any) -> SemanticModel:
        if len(query) == 1 and isinstance(query[0], SemanticModelMeta):
            rep = query[0]
            if getattr(rep, "_semantic_role", None) == "representation":
                exact = [d.value for d in self._data.get(subject.uid, []) if d.representation is rep]
                if not exact:
                    raise KeyError(f"no {rep.__name__} for {subject.uid}")
                if len(exact) > 1:
                    raise AmbiguousSemanticMatch(rep.__name__)
                return exact[0]
        found = self.find(subject, *query)
        if not found:
            raise KeyError(f"no semantic match for {subject.uid}: {sem(*query)}")
        if len(found) > 1:
            raise AmbiguousSemanticMatch(
                f"{subject.uid}: {sem(*query)} -> {[type(x).__name__ for x in found]}"
            )
        return found[0]

    def get_many(self, subjects: Iterable[ModelRef], *query: Any) -> dict[str, SemanticModel]:
        return {subject.uid: self.get(subject, *query) for subject in subjects}

    def relate(self, relation: RelationType, *operands: ModelRef) -> RelationFact:
        fact = relation(*operands)
        self._relations.append(fact)
        return fact

    def relations(self, relation: RelationType | None = None) -> list[RelationFact]:
        if relation is None:
            return list(self._relations)
        return [fact for fact in self._relations if fact.relation == relation]


def value_semantics(value: SemanticModel) -> Product:
    out = type(value)._semantics
    if is_dataclass(value):
        for field in fields(value):
            item = getattr(value, field.name)
            if isinstance(item, SemanticEnum):
                out = out | item._semantics
    return out
