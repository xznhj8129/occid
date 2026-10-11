from __future__ import annotations

from copy import copy, deepcopy
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
from math import isfinite
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterable
from uuid import UUID, uuid4

import msgpack

from .definitions import load_definitions, prepare, product_terms, SECTIONS

MAX_SOLVER_DEPTH = 48
MAX_CANDIDATES = 128


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
        else:
            out = out | Product(frozenset({semantic_name(term)}))
    return out


class UID(bytes):
    """Exact binary identity; readable names and external references are strings."""

    def __new__(cls, value: bytes):
        if not isinstance(value, bytes) or len(value) != 16:
            raise ValueError("UID requires exactly 16 bytes")
        return super().__new__(cls, value)

    @classmethod
    def new(cls) -> "UID":
        return cls(uuid4().bytes)

    def __str__(self) -> str:
        return str(UUID(bytes=bytes(self)))


class Expr:
    def evaluate(self, terms: frozenset[str]) -> bool:
        raise NotImplementedError

    def forced_terms(self) -> set[str]:
        return set()


@dataclass(frozen=True, slots=True)
class Term(Expr):
    name: str

    def evaluate(self, terms: frozenset[str]) -> bool:
        return self.name in terms

    def forced_terms(self) -> set[str]:
        return {self.name}

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True, slots=True)
class All(Expr):
    items: tuple[Expr, ...]

    def evaluate(self, terms: frozenset[str]) -> bool:
        return all(item.evaluate(terms) for item in self.items)

    def forced_terms(self) -> set[str]:
        out: set[str] = set()
        for item in self.items:
            out |= item.forced_terms()
        return out

    def __str__(self) -> str:
        return f"ALL({', '.join(str(x) for x in self.items)})"


@dataclass(frozen=True, slots=True)
class Any(Expr):
    items: tuple[Expr, ...]

    def evaluate(self, terms: frozenset[str]) -> bool:
        return any(item.evaluate(terms) for item in self.items)

    def __str__(self) -> str:
        return f"ANY({', '.join(str(x) for x in self.items)})"


@dataclass(frozen=True, slots=True)
class Not(Expr):
    item: Expr

    def evaluate(self, terms: frozenset[str]) -> bool:
        return not self.item.evaluate(terms)

    def __str__(self) -> str:
        return f"NOT({self.item})"


TRUE = All(())
FALSE = Any(())


def parse_expr(data: Any, axis_values: dict[str, list[str]] | None = None) -> Expr:
    if data is None:
        return TRUE
    if isinstance(data, Expr):
        return data
    if isinstance(data, bool):
        return TRUE if data else FALSE
    if isinstance(data, str):
        return Term(data)
    if isinstance(data, list):
        return All(tuple(parse_expr(x, axis_values) for x in data))
    if isinstance(data, dict):
        if "term" in data:
            return Term(str(data["term"]))
        if "axis" in data:
            # Compact authoring form: any value of the axis is present.
            values = (axis_values or {}).get(str(data["axis"]), [])
            return Any(tuple(Term(x) for x in values))
        if "all" in data:
            return All(tuple(parse_expr(x, axis_values) for x in data["all"]))
        if "any" in data:
            return Any(tuple(parse_expr(x, axis_values) for x in data["any"]))
        if "not" in data:
            return Not(parse_expr(data["not"], axis_values))
        if "const" in data:
            return TRUE if data["const"] else FALSE
    raise ValueError(f"not a rule expression: {data!r}")


@dataclass(frozen=True, slots=True)
class Rule:
    name: str
    kind: str
    when: Expr = TRUE
    then: Expr = TRUE
    left: Expr = TRUE
    right: Expr = TRUE
    profiles: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Coord:
    name: str
    type: str | None
    unit: str | None = None
    optional: bool = False
    semantics: Product = EMPTY
    many: bool = False
    vocabulary: str | None = None
    values: tuple[tuple[str, Product], ...] = ()
    qualifiers: Product = EMPTY
    has_default: bool = False
    default: Any = None
    inherit: tuple[str, ...] = ()

    def __str__(self) -> str:
        region = str(self.semantics) if self.semantics.terms else self.type
        return f"{self.name}:{region}" + (f"[{self.unit}]" if self.unit else "") + ("*" if self.many else "")


@dataclass(frozen=True, slots=True)
class ChartType:
    display: str
    factors: Product
    coords: tuple[Coord, ...]
    _context: dict = field(default_factory=dict, repr=False)
    ordered: tuple[tuple[str, str], ...] = ()

    def __post_init__(self):
        object.__setattr__(self, "_context", deepcopy(self._context))

    @property
    def context(self) -> dict:
        return deepcopy(self._context)

    def __str__(self) -> str:
        body = " * ".join(str(coord) for coord in self.coords)
        return f"chart {self.display} := {body}"


# ---------------------------------------------------------------------------
# Open expressions: fixed factors + typed free variables + equations.
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Equation:
    quantity: str
    of: str
    equals: str

    def __str__(self) -> str:
        return f"{self.quantity}({self.of}) = {self.equals}"


@dataclass(frozen=True, slots=True)
class ExpressionType:
    name: str
    factors: Product
    given: dict[str, Product]
    sought: dict[str, Product]
    equations: tuple[Equation, ...]
    words: tuple[str, ...]
    roles: dict[str, Product] = field(default_factory=dict)

    def __post_init__(self):
        object.__setattr__(self, "given", MappingProxyType(dict(self.given)))
        object.__setattr__(self, "sought", MappingProxyType(dict(self.sought)))
        object.__setattr__(self, "roles", MappingProxyType(dict(self.roles)))

    @property
    def variables(self) -> dict[str, Product]:
        return {**self.given, **self.sought}

    def __str__(self) -> str:
        given = ", ".join(
            f"{role}: {' * '.join(sorted(region.terms)) or '∅'}"
            for role, region in self.given.items()
        )
        text = f"{self.name}({given})"
        if self.sought:
            sought = ", ".join(
                f"{role}: {' * '.join(sorted(region.terms)) or '∅'}"
                for role, region in self.sought.items()
            )
            text += f" => {sought}"
        if self.equations:
            text += "  { " + "; ".join(str(eq) for eq in self.equations) + " }"
        return text


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


@dataclass(frozen=True, slots=True)
class Axis:
    registry: "SemanticRegistry"
    name: str

    def __getattr__(self, value: str) -> AxisValue:
        if f"{self.name}.{value}" not in self.registry.axis_of_value:
            raise AttributeError(f"axis {self.name} has no value {value!r}")
        return AxisValue(self.name, value)

    def __str__(self) -> str:
        return self.name


class SemanticSolverLimit(RuntimeError):
    pass


class AmbiguousSemanticMatch(LookupError):
    pass


class IllegalSemanticCombination(ValueError):
    pass


class _Source(Enum):
    ANY = "any source"


def _time_key(value: Any) -> tuple[str, Any]:
    """Numeric source clocks and offset-aware UTC instants are distinct domains."""
    if isinstance(value, (int, float)) and not isinstance(value, bool) and isfinite(value):
        return "numeric", value
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if isinstance(value, datetime) and value.utcoffset() is not None:
        return "instant", value.astimezone(timezone.utc)
    raise ValueError(f"time must be finite numeric or an offset-aware ISO instant: {value!r}")


def _compare_time(left: Any, right: Any) -> int:
    left_domain, left_value = _time_key(left)
    right_domain, right_value = _time_key(right)
    if left_domain != right_domain:
        raise AmbiguousSemanticMatch("cannot compare numeric source clocks with UTC instants")
    return (left_value > right_value) - (left_value < right_value)


@dataclass(frozen=True)
class Query:
    """A semantic question with explicit evidence and interpretation constraints."""
    semantics: Product = EMPTY
    source: Any = _Source.ANY
    provenance: dict | None = None
    observed_before: Any = None
    valid_at: Any = None
    latest: bool = False
    interpretation: str = "current"
    contains: tuple[Product, ...] = ()
    unit: str | None = None

    def __post_init__(self):
        object.__setattr__(self, "semantics", sem(self.semantics))
        object.__setattr__(self, "source", deepcopy(self.source))
        object.__setattr__(self, "contains", tuple(sem(region) for region in self.contains))
        if self.provenance is not None:
            if not isinstance(self.provenance, dict):
                raise TypeError("query provenance must be a mapping")
            object.__setattr__(self, "provenance", deepcopy(self.provenance))
        if self.interpretation not in ("current", "recorded"):
            raise ValueError("query interpretation must be current or recorded")
        if not isinstance(self.latest, bool):
            raise TypeError("query latest must be boolean")
        for value in (self.observed_before, self.valid_at):
            if value is not None:
                _time_key(value)

    def narrow(self, region: Product) -> "Query":
        return replace(self, semantics=self.semantics | region)

    @property
    def constrained_evidence(self) -> bool:
        return self.source != _Source.ANY or self.provenance is not None or self.observed_before is not None or self.valid_at is not None or self.latest or bool(self.contains) or self.unit is not None

    def accepts(self, datum: "Datum") -> bool:
        if self.unit is not None and datum.unit != self.unit:
            return False
        if self.source != _Source.ANY and datum.source != self.source:
            return False
        if self.provenance is not None:
            actual = datum.provenance
            if any(key not in actual or actual[key] != value for key, value in self.provenance.items()):
                return False
        if self.observed_before is not None:
            if datum.observed_at is None or _compare_time(datum.observed_at, self.observed_before) > 0:
                return False
        if self.valid_at is not None:
            interval = datum.validity
            if not isinstance(interval, dict) or not interval.keys() & {"from", "to", "until"}:
                return False
            if "to" in interval and "until" in interval and interval["to"] != interval["until"]:
                raise ValueError(f"fact {datum.id}: conflicting validity endpoints")
            for name in ("from", "to", "until"):
                if name in interval:
                    if interval[name] is None:
                        return False
                    order = _compare_time(self.valid_at, interval[name])
                    if (name == "from" and order < 0) or (name != "from" and order >= 0):
                        return False
        return True

    def select(self, found: list["Datum"]) -> list["Datum"]:
        if not self.latest or not found:
            return found
        if any(datum.observed_at is None for datum in found):
            raise AmbiguousSemanticMatch("latest observation is unknown: a matching fact has no observation time")
        if _time_key(found[0].observed_at)[0] == "numeric" and any(datum.source != found[0].source for datum in found[1:]):
            raise AmbiguousSemanticMatch("latest observation requires comparable source clocks; constrain the source or supply UTC instants")
        newest = found[0].observed_at
        for datum in found[1:]:
            if _compare_time(datum.observed_at, newest) > 0:
                newest = datum.observed_at
        return [datum for datum in found if _compare_time(datum.observed_at, newest) == 0]


def _question(registry: "SemanticRegistry", terms: tuple[Any, ...]) -> Query:
    questions = [term for term in terms if isinstance(term, Query)]
    if len(questions) > 1:
        raise TypeError("a semantic question accepts one Query")
    question = questions[0] if questions else Query()
    region = registry.product(*(term for term in terms if not isinstance(term, Query)))
    question = replace(question, semantics=registry.product(question.semantics) | region,
                       contains=tuple(registry.product(region) for region in question.contains))
    for product in (question.semantics, *question.contains):
        if not registry.legal(product):
            raise IllegalSemanticCombination(f"illegal semantic query: {product}")
    return question


@dataclass(frozen=True)
class Datum:
    """One immutable observation, with its original definition revision."""
    id: str
    subject: str | bytes
    semantics: Product
    meaning: Product
    definition_id: str
    _value: Any = field(repr=False)
    _definitions: "DefinitionRevision" = field(repr=False)
    _source: Any = field(default=None, repr=False)
    _observed_at: Any = field(default=None, repr=False)
    _validity: Any = field(default=None, repr=False)
    _provenance: dict = field(default_factory=dict, repr=False)
    _extensions: dict = field(default_factory=dict, repr=False)
    partial: bool = False
    unit: str | None = None

    def __post_init__(self):
        if isinstance(self._definitions, dict):
            object.__setattr__(self, "_definitions", DefinitionRevision(self._definitions))
        for name in ("_value", "_source", "_observed_at", "_validity", "_provenance", "_extensions"):
            object.__setattr__(self, name, deepcopy(getattr(self, name)))

    @property
    def value(self):
        return deepcopy(self._value)

    @property
    def definitions(self):
        return self._definitions.spec

    @property
    def source(self):
        return deepcopy(self._source)

    @property
    def observed_at(self):
        return deepcopy(self._observed_at)

    @property
    def validity(self):
        return deepcopy(self._validity)

    @property
    def provenance(self):
        return deepcopy(self._provenance)

    @property
    def extensions(self):
        return deepcopy(self._extensions)

    def encode(self, *, include_definitions: bool = True) -> bytes:
        from .wire import encode
        return encode(self, include_definitions=include_definitions)

    def decompose(self, *, registry: "SemanticRegistry | None" = None) -> "Component":
        registry = registry or self._definitions.registry()
        return registry.decompose(self.semantics, self.value, datum=self, partial=self.partial, _unit=self.unit)

    def find(self, *query: Any) -> list["Component"]:
        return self.decompose().find(*query)

    def get(self, *query: Any) -> "Component":
        return self.decompose().get(*query)


@dataclass(frozen=True)
class SemanticValue:
    """A value inhabiting a product. Charts, not this carrier, define its parts."""
    semantics: Product
    _value: Any = field(repr=False)
    partial: bool = False
    unit: str | None = None

    def __post_init__(self):
        object.__setattr__(self, "semantics", sem(self.semantics))
        object.__setattr__(self, "_value", deepcopy(self._value))
        if type(self.partial) is not bool:
            raise TypeError("semantic value partial must be boolean")
        if self.unit is not None and not isinstance(self.unit, str):
            raise TypeError("semantic value unit must be text")

    @property
    def value(self):
        return deepcopy(self._value)


@dataclass(frozen=True)
class Binding:
    """A chart variable bound to zero, one, or an ordered sequence of values."""
    variable: Coord
    components: tuple["Component", ...]
    present: bool = True
    null: bool = False


@dataclass(frozen=True)
class Component:
    """A chart projection: intrinsic meaning, role, order, and evidence identity.

    Parent and child products describe different things. Their connection is a
    typed variable binding, never multiplication of the two things' meanings.
    """
    semantics: Product
    meaning: Product
    _registry: "SemanticRegistry" = field(repr=False, compare=False)
    _primitive: Any = field(default=None, repr=False)
    bindings: tuple[Binding, ...] = ()
    structured: bool = False
    _extras: dict = field(default_factory=dict, repr=False)
    variable: Coord | None = None
    ordinal: int | None = None
    defaulted: bool = False
    _tagged: bool = False
    _path: tuple = field(default=(), repr=False)
    _datum: Datum | None = field(default=None, repr=False, compare=False)
    _tag_product: Product | None = field(default=None, repr=False)
    _tag_partial: bool = field(default=False, repr=False)
    _tag_unit: str | None = field(default=None, repr=False)
    _unit: str | None = field(default=None, repr=False)

    @property
    def id(self):
        return (self._datum.id if self._datum else None, self._path)

    @property
    def unit(self):
        return self._unit if self._unit is not None else self.variable.unit if self.variable else None

    @property
    def source(self):
        return self._datum.source if self._datum else None

    @property
    def observed_at(self):
        return self._datum.observed_at if self._datum else None

    @property
    def validity(self):
        return self._datum.validity if self._datum else None

    @property
    def provenance(self):
        return self._datum.provenance if self._datum else {}

    @property
    def interpretation_id(self):
        return self._registry.definition_id

    @property
    def value(self):
        return self.recompose()

    def walk(self):
        yield self
        for binding in self.bindings:
            for component in binding.components:
                yield from component.walk()

    def leaves(self) -> list["Component"]:
        return [component for component in self.walk() if not component.structured]

    def find(self, *query: Any) -> list["Component"]:
        question = _question(self._registry, query)
        return question.select([component for component in self.walk() if question.semantics.terms <= component.meaning.terms and component.contains(question.contains) and question.accepts(component)])

    def contains(self, regions: Iterable[Product]) -> bool:
        """Existential part constraints require distinct binding occurrences."""
        descendants = list(self.walk())[1:]
        occupied = {}

        def assign(region_index, visited):
            for index, part in enumerate(descendants):
                if index in visited or not regions[region_index].terms <= part.meaning.terms:
                    continue
                visited.add(index)
                if index not in occupied or assign(occupied[index], visited):
                    occupied[index] = region_index
                    return True
            return False

        regions = tuple(regions)
        return all(assign(index, set()) for index in range(len(regions)))

    @property
    def complete(self) -> bool:
        return all((binding.present or binding.variable.optional or binding.variable.has_default)
                   and all(part.complete for part in binding.components) for binding in self.bindings)

    def project(self, *queries: Any) -> "Component":
        """Select semantic subexpressions while retaining their binding incidence.

        This is an explicit projection. Unselected values remain in the source
        datum; a projected required variable may be unbound.
        """
        questions = [_question(self._registry, (query,)) for query in queries]
        selected = {part.id for question in questions for part in self.find(question)}

        def select(node):
            if node.id in selected:
                return node
            bindings = []
            for binding in node.bindings:
                parts = tuple(part for child in binding.components if (part := select(child)) is not None)
                bindings.append(Binding(binding.variable, parts, bool(parts)))
            if not any(binding.components for binding in bindings):
                return None
            return replace(node, bindings=tuple(bindings), _extras={})

        return select(self) or replace(self, bindings=tuple(Binding(binding.variable, (), False) for binding in self.bindings), _extras={})

    def get(self, *query: Any) -> "Component":
        found = self.find(*query)
        if not found:
            raise KeyError(f"no component satisfies {query!r}")
        if len(found) != 1:
            raise AmbiguousSemanticMatch(f"{query!r} matches component identities {[component.id for component in found]}")
        return found[0]

    def recompose(self, parts: Iterable["Component"] | None = None):
        """Invert this chart, preserving roles, repeated values, and unknown data.

        Supplying leaves requires every non-default leaf of this composition;
        identities carry the binding incidence and sequence order. Missing or
        foreign leaves are rejected, rather than silently discarded.
        """
        replacements = None
        if parts is not None:
            parts = list(parts)
            replacements = {part.id: part for part in parts}
            expected = {part.id for part in self.leaves() if not part.defaulted}
            actual = {part.id for part in parts if not part.defaulted}
            if len(replacements) != len(parts) or expected != actual:
                raise ValueError(f"recomposition requires exactly its leaves; missing={expected - actual}, foreign={actual - expected}")
        return self._recompose(replacements)

    def _recompose(self, replacements):
        if not self.structured:
            part = replacements[self.id] if replacements is not None and not self.defaulted else self
            return deepcopy(part._primitive)
        result = deepcopy(self._extras)
        for binding in self.bindings:
            if not binding.present:
                continue
            if binding.null:
                result[binding.variable.name] = None
                continue
            values = []
            for part in binding.components:
                value = part._recompose(replacements)
                if part._tagged:
                    value = SemanticValue(part._tag_product or part.semantics, value, part._tag_partial, part._tag_unit)
                values.append(value)
            result[binding.variable.name] = values if binding.variable.many else values[0]
        return result

    def links(self) -> list["RelationFact"]:
        relation = self._registry.relation_types["HasComponent"]
        return [relation(whole=node, part=part) for node in self.walk() for binding in node.bindings for part in binding.components if part.meaning.terms and "Root" in part.meaning]

    @property
    def expression(self) -> ExpressionType:
        if self.variable is None or self.variable.type != "word":
            raise TypeError("component is not an expression word")
        return self._registry.expression_of(self.value)

    def referent(self, store: "Store") -> "SubjectRef":
        if self.variable is None or self.variable.type != "reference":
            raise TypeError("component is not a reference binding")
        uid = subject_identity(self.value)
        if uid not in store._subjects:
            raise KeyError(f"unknown referent {uid!r}")
        return SubjectRef(store, uid)


@dataclass(frozen=True, slots=True)
class RelationType:
    name: str
    signature: tuple[Product, ...]
    operand_names: tuple[str, ...]
    definition_id: str
    specializes: "RelationType | None" = None

    def is_a(self, other: "RelationType") -> bool:
        current = self
        while current is not None:
            if current.name == other.name:
                return True
            current = current.specializes
        return False

    def __call__(self, *operands: "SubjectRef", **roles: "SubjectRef") -> "RelationFact":
        if roles:
            if operands or roles.keys() != set(self.operand_names):
                raise TypeError(f"{self.name} expects named roles {self.operand_names}")
            operands = tuple(roles[name] for name in self.operand_names)
        if len(operands) != len(self.signature):
            raise TypeError(f"{self.name} expects {len(self.signature)} operands")
        for role, operand, expected in zip(self.operand_names, operands, self.signature):
            if not isinstance(operand, (SubjectRef, Datum, Component)) or not expected.terms <= value_semantics(operand).terms:
                raise TypeError(f"{self.name} operand {role!r} expects {expected}, got {operand!r}")
        subjects = [operand for operand in operands if isinstance(operand, SubjectRef)]
        if subjects and any(operand.store is not subjects[0].store for operand in subjects):
            raise ValueError(f"{self.name}: operands belong to different stores")
        return RelationFact(str(uuid4()), self, tuple(operands))


@dataclass(frozen=True, slots=True)
class RelationFact:
    id: str
    relation: RelationType
    operands: tuple["SubjectRef", ...]

    @property
    def roles(self) -> dict[str, "SubjectRef"]:
        return dict(zip(self.relation.operand_names, self.operands))

    def __str__(self) -> str:
        parts = (f"{role}={operand.uid if isinstance(operand, SubjectRef) else operand.id}" for role, operand in zip(self.relation.operand_names, self.operands))
        return f"{self.relation.name}({', '.join(parts)})"


def definition_identity(spec: dict) -> str:
    # Map order matters for relation operand order; do not sort it away.
    return sha256(msgpack.packb(spec, use_bin_type=True)).hexdigest()


@dataclass(frozen=True)
class DefinitionRevision:
    """One shared definition snapshot; observations retain this original model."""
    _spec: dict = field(repr=False)
    id: str = field(init=False)
    _registry: "SemanticRegistry | None" = field(default=None, repr=False, compare=False)

    def __post_init__(self):
        object.__setattr__(self, "_spec", deepcopy(self._spec))
        object.__setattr__(self, "id", definition_identity(self._spec))

    @property
    def spec(self) -> dict:
        return deepcopy(self._spec)

    def registry(self) -> "SemanticRegistry":
        if self._registry is None:
            model = SemanticRegistry(self._spec)
            model._readonly = True
            object.__setattr__(self, "_registry", model)
        return self._registry


class SemanticRegistry:
    def __init__(self, spec: dict[str, Any]):
        self._revision = DefinitionRevision(spec)
        self._spec = self._revision._spec
        data = prepare(spec)
        self.primitive_types = {name: item["primitive"] for name, item in data["factors"].items() if "primitive" in item}
        self.definition_id = self._revision.id
        self._history = {self.definition_id: self._revision}
        self._revisions = {}
        self._readonly = False
        self.aliases = data["aliases"]
        self.axis_of_value = {}
        self.axis_cardinality = {}
        self.axis_region = {}
        axis_values = {}
        for name, axis in data["axes"].items():
            values = [f"{name}.{value}" for value in axis["values"]]
            axis_values[name] = values
            self.axis_cardinality[name] = axis.get("cardinality", "many")
            self.axis_of_value.update({value: name for value in values})

        self.rules = []
        for name, axis in data["axes"].items():
            self._add_declarations(name, Any(tuple(Term(value) for value in axis_values[name])), axis, axis_values, name)
            for value, declaration in axis["value_meta"].items():
                self._add_declarations(f"{name}.{value}", Term(f"{name}.{value}"), declaration, axis_values)
        for name, factor in data["factors"].items():
            self._add_declarations(name, Term(name), factor, axis_values)
        self.active_rules = self.rules
        self.term_applicability = {}
        for rule in self.rules:
            if rule.kind == "applicability" and isinstance(rule.when, Term):
                self.term_applicability.setdefault(rule.when.name, []).append(rule.then)

        self.charts = [
            ChartType(
                item["display"],
                product_names(item["factors"]),
                tuple(Coord(
                    name=coord["name"], type=coord.get("type"), unit=coord.get("unit"),
                    optional=bool(coord.get("optional")), semantics=product_names(coord["semantics"]),
                    many=coord.get("many", False), vocabulary=coord.get("vocabulary"),
                    values=tuple((name, product_names(region)) for name, region in coord.get("values", {}).items()),
                    qualifiers=product_names(coord.get("qualifiers", [])),
                    has_default="default" in coord, default=coord.get("default"),
                    inherit=tuple(coord.get("inherit", [])),
                ) for coord in item["coords"]),
                item["context"],
                tuple(tuple(pair) for pair in item["ordered"]),
            )
            for item in data["charts"]
        ]
        self.expressions = {name: ExpressionType(name, product_names(item["factors"]), {role: product_names(region) for role, region in item["given"].items()}, {role: product_names(region) for role, region in item["sought"].items()}, tuple(Equation(**equation) for equation in item["equations"]), tuple(item["words"]), {role: product_names(region) for role, region in item["roles"].items()}) for name, item in data["expressions"].items()}
        self.word_expressions = data["word_expressions"]
        self._mappings = data["mappings"]
        self.vocabularies = data["vocabularies"]
        self.relation_types = {}
        for name in data["relations"]:
            self._relation(name, data["relations"])
        self._validate(data)
        self.aliases = MappingProxyType({name: tuple(terms) for name, terms in self.aliases.items()})
        self.axis_of_value = MappingProxyType(self.axis_of_value)
        self.axis_cardinality = MappingProxyType(self.axis_cardinality)
        self.axis_region = MappingProxyType(self.axis_region)
        self.rules = tuple(self.rules)
        self.active_rules = self.rules
        self.term_applicability = MappingProxyType({name: tuple(regions) for name, regions in self.term_applicability.items()})
        self.charts = tuple(self.charts)
        self.expressions = MappingProxyType(self.expressions)
        self.word_expressions = MappingProxyType(self.word_expressions)
        self.relation_types = MappingProxyType(self.relation_types)
        self.vocabularies = MappingProxyType({name: MappingProxyType(members) for name, members in self.vocabularies.items()})
        self.primitive_types = MappingProxyType(self.primitive_types)
        recorded = copy(self)
        recorded._readonly = True
        object.__setattr__(self._revision, "_registry", recorded)

    @classmethod
    def load(cls, path: str | Path) -> "SemanticRegistry":
        return cls(load_definitions(path))

    @property
    def spec(self) -> dict:
        return deepcopy(self._spec)

    @property
    def mappings(self) -> dict:
        return deepcopy(self._mappings)

    def update(self, changes: dict) -> None:
        if self._readonly:
            raise ValueError("a recorded definition revision cannot be updated")
        if not isinstance(changes, dict) or changes.keys() - set(SECTIONS):
            raise ValueError(f"definition updates must name sections {SECTIONS}")
        revised = self.spec
        for section, entries in changes.items():
            if not isinstance(entries, dict):
                raise ValueError(f"definition update {section}: expected mapping")
            revised.setdefault(section, {}).update(deepcopy(entries))
        candidate = SemanticRegistry(revised)
        history = {**self._history, candidate.definition_id: candidate._revision}
        revisions = self._revisions
        self.__dict__.update(candidate.__dict__)
        self._history = history
        self._revisions = revisions

    def at(self, definition_id: str) -> "SemanticRegistry":
        if definition_id not in self._revisions:
            self._revisions[definition_id] = self._history[definition_id].registry()
        return self._revisions[definition_id]

    def product(self, *terms: Any) -> Product:
        result = []
        for term in sem(*terms):
            for name in product_terms(term):
                if name in self.word_expressions:
                    result.extend(self.expressions[self.word_expressions[name]].factors)
                else:
                    result.extend(self.aliases.get(name, [name]))
        return product_names(result)

    def axis(self, name: str) -> Axis:
        if name not in self.axis_cardinality:
            raise KeyError(f"unknown axis {name!r}")
        return Axis(self, name)

    def expression_of(self, word: str) -> ExpressionType:
        return self.expressions[self.word_expressions.get(word, word)]

    def _add_declarations(self, owner, when, declaration, axis_values, axis_scope=None):
        for key, kind in (("applies", "applicability"), ("requires", "requirement"), ("implies", "implication")):
            if key in declaration:
                region = parse_expr(declaration[key], axis_values)
                self.rules.append(Rule(f"{owner}.{key}", kind, when=when, then=region))
                if key == "applies" and axis_scope is not None:
                    self.axis_region[axis_scope] = region
        for index, right in enumerate(declaration.get("disjoint", [])):
            self.rules.append(Rule(f"{owner}.disjoint.{index}", "disjointness", left=when, right=parse_expr(right, axis_values)))
        for index, group in enumerate(declaration.get("excludes", [])):
            self.rules.append(Rule(f"{owner}.excludes.{index}", "exclusion", when=All((when, parse_expr(group, axis_values)))))

    def _relation(self, name, declarations, trail=()):
        if name in trail:
            raise ValueError(f"relation specialization cycle: {' -> '.join((*trail, name))}")
        if name not in declarations:
            raise ValueError(f"unknown relation {name!r}")
        if name not in self.relation_types:
            item = declarations[name]
            parent = self._relation(item["specializes"], declarations, (*trail, name)) if item.get("specializes") else None
            signature = tuple(self.closure(product_names(region)) for region in item["operands"].values())
            if parent and (len(signature) != len(parent.signature) or any(not base.terms <= region.terms for region, base in zip(signature, parent.signature))):
                raise ValueError(f"relation {name}: specialization must narrow operands positionally")
            self.relation_types[name] = RelationType(name, signature, tuple(item["operands"]), self.definition_id, parent)
        return self.relation_types[name]

    def _validate(self, data):
        regions = [self.product(name) for name in data["factors"]]
        regions += [self.product(name) for name in self.axis_of_value]
        regions += [self.product(name) for name in self.aliases]
        regions += [chart.factors for chart in self.charts]
        for expression in self.expressions.values():
            regions += [expression.factors, *expression.variables.values()]
            regions += [region | expression.roles.get(name, EMPTY) for name, region in expression.variables.items()]
            for equation in expression.equations:
                if not self.entails(self.product(equation.quantity), expression.variables[equation.equals]):
                    raise ValueError(f"expression {expression.name}: equation result violates variable region")
        for relation in self.relation_types.values():
            regions += list(relation.signature)
        regions += [product_names(item["semantics"]) for item in self.mappings.values()]
        for region in regions:
            if not self.legal(region):
                raise IllegalSemanticCombination(f"definition declares an illegal semantic region: {region}")
        for chart in self.charts:
            self.coordinates(chart.factors)
            for coordinate in chart.coords:
                if coordinate.semantics.terms and not self.legal(coordinate.semantics | coordinate.qualifiers):
                    raise ValueError(f"chart {chart.display}: illegal variable region {coordinate.semantics}")
                for member, region in coordinate.values:
                    if coordinate.vocabulary is None or member not in self.vocabularies[coordinate.vocabulary]:
                        raise ValueError(f"chart {chart.display}: unknown vocabulary value {member!r}")
                    if not self.legal(coordinate.semantics | coordinate.qualifiers | region):
                        raise ValueError(f"chart {chart.display}: illegal value region {region}")
                if coordinate.has_default:
                    self._coordinate_product(coordinate, coordinate.default)
        for word in self.word_expressions:
            vocabulary, member = word.split(".")
            if vocabulary in self.vocabularies and member not in self.vocabularies[vocabulary]:
                raise ValueError(f"word {word!r} is outside its declared vocabulary")

    def coordinates(self, product: Product) -> dict[str, Coord]:
        result = {}
        for chart in self.charts:
            if self.entails(product, chart.factors):
                for coordinate in chart.coords:
                    previous = result.get(coordinate.name)
                    if previous is not None and previous != coordinate:
                        raise ValueError(f"conflicting charts for {product}: coordinate {coordinate.name}")
                    result[coordinate.name] = coordinate
        return result

    def _coordinate_product(self, coordinate: Coord, value: Any) -> Product:
        product = coordinate.semantics | coordinate.qualifiers
        if isinstance(value, SemanticValue):
            if not self.entails(value.semantics, coordinate.semantics):
                raise TypeError(f"{coordinate.name}: {value.semantics} does not satisfy {coordinate.semantics}")
            product |= self.product(value.semantics)
            if value.unit is not None and coordinate.unit != value.unit:
                raise ValueError(f"{coordinate.name}: source unit {value.unit!r} differs from chart unit {coordinate.unit!r}; an explicit conversion is required")
            value = value.value
        if value is None and coordinate.optional:
            return product
        kind = coordinate.type
        if kind in PRIMITIVE_TYPES:
            valid = (type(value) in (int, float) and isfinite(value)) if kind == "float" else type(value) is PRIMITIVE_TYPES[kind]
            if not valid:
                raise TypeError(f"{coordinate.name}={value!r} requires {coordinate}")
        elif kind in ("identity", "reference"):
            subject_identity(value)
        elif kind == "product":
            if not isinstance(value, (str, Product)):
                raise TypeError(f"{coordinate.name}: expected a semantic description")
            if not self.legal(self.product(value)):
                raise IllegalSemanticCombination(f"{coordinate.name}: illegal semantic description {value}")
        elif kind == "word":
            if not isinstance(value, str) or value not in self.word_expressions:
                raise ValueError(f"{coordinate.name}: unknown expression word {value!r}")
            vocabulary = coordinate.vocabulary
            if vocabulary and not value.startswith(vocabulary + "."):
                raise TypeError(f"{coordinate.name}: word must belong to {vocabulary}")
        elif kind == "code":
            members = self.vocabularies[coordinate.vocabulary]
            matches = [name for name, code in members.items() if (type(value) is str and value in (name, coordinate.vocabulary + "." + name)) or (type(value) is type(code) and value == code)]
            if len(matches) != 1:
                raise ValueError(f"{coordinate.name}: {value!r} is not an unambiguous {coordinate.vocabulary} value")
            product |= dict(coordinate.values).get(matches[0], EMPTY)
        if not self.legal(product):
            raise IllegalSemanticCombination(f"{coordinate.name}: illegal component product {product}")
        return product

    def validate_value(self, product: Product, value: Any, *, partial: bool = False) -> None:
        self.decompose(product, value, partial=partial)

    def decompose(self, product: Any, value: Any, *, datum: Datum | None = None, partial: bool = False,
                  _variable: Coord | None = None, _path: tuple = (), _qualifiers: Product = EMPTY,
                  _ordinal: int | None = None, _defaulted: bool = False, _unit: str | None = None) -> Component:
        """Reduce a product through its charts to typed, addressable bindings."""
        product = self.product(product)
        tagged = isinstance(value, SemanticValue)
        if tagged:
            if not self.entails(value.semantics, product):
                raise TypeError(f"{value.semantics} does not satisfy {product}")
            product |= self.product(value.semantics)
            partial = partial or value.partial
            _unit = value.unit
            value = value.value
        product |= _qualifiers
        if not self.legal(product):
            raise IllegalSemanticCombination(f"illegal component product {product}")
        coordinates = self.coordinates(product)
        if not coordinates:
            for name, kind in self.primitive_types.items():
                if self.entails(product, name):
                    self._coordinate_product(Coord(name, kind, semantics=self.product(name)), value)
        bindings = []
        if coordinates:
            if not isinstance(value, dict):
                raise TypeError(f"{product}: chart value must be a mapping")
            for name, coordinate in coordinates.items():
                present = name in value
                if not present and not coordinate.has_default:
                    if not coordinate.optional and not partial:
                        raise ValueError(f"{product}: missing coordinate {name!r}")
                    bindings.append(Binding(coordinate, (), False))
                    continue
                item = value[name] if present else coordinate.default
                if item is None and coordinate.optional:
                    bindings.append(Binding(coordinate, (), present, True))
                    continue
                if coordinate.many and not isinstance(item, list):
                    raise TypeError(f"{product}: {name} requires an ordered list")
                items = item if coordinate.many else [item]
                parts = []
                for ordinal, item in enumerate(items):
                    region = self._coordinate_product(coordinate, item)
                    # Only declared qualifiers propagate. A parent's quantity
                    # is not the quantity of its parts; position is not latitude.
                    inherited = _qualifiers | coordinate.qualifiers | product_names(term for term in product if self.axis_of_value.get(term) in coordinate.inherit)
                    region |= inherited
                    part = self.decompose(region, item.value if isinstance(item, SemanticValue) else item,
                                          datum=datum, partial=partial, _variable=coordinate,
                                          _path=(*_path, name, ordinal) if coordinate.many else (*_path, name),
                                          _qualifiers=inherited, _ordinal=ordinal if coordinate.many else None,
                                          _defaulted=not present, _unit=item.unit if isinstance(item, SemanticValue) else None)
                    if isinstance(item, SemanticValue):
                        part = replace(part, _tagged=True, _tag_product=item.semantics, _tag_partial=item.partial, _tag_unit=item.unit)
                    parts.append(part)
                bindings.append(Binding(coordinate, tuple(parts), present))
            for chart in self.charts:
                if self.entails(product, chart.factors):
                    for lower, upper in chart.ordered:
                        low = value.get(lower)
                        high = value.get(upper)
                        low = low.value if isinstance(low, SemanticValue) else low
                        high = high.value if isinstance(high, SemanticValue) else high
                        if low is not None and high is not None and low > high:
                            raise ValueError(f"{product}: {lower} must not exceed {upper}")
        return Component(product, self.closure(product), self, deepcopy(value) if not coordinates else None,
                         tuple(bindings), bool(coordinates) and value is not None,
                         {key: deepcopy(item) for key, item in value.items() if key not in coordinates} if coordinates and isinstance(value, dict) else {},
                         _variable, _ordinal, _defaulted, tagged, _path, datum, _unit=_unit)

    def compose(self, product: Any, *parts: SemanticValue | Component, partial: bool = False) -> SemanticValue:
        """Bind chart variables by semantic region, independent of field spelling.

        Many-valued variables consume matching parts in caller order. A part
        matching two distinct roles is ambiguous and needs a role qualifier.
        """
        product = self.product(product)
        coordinates = self.coordinates(product)
        bindings = {name: [] for name in coordinates}
        for part in parts:
            if not isinstance(part, (SemanticValue, Component)):
                raise TypeError("composition requires semantic values or components")
            region = self.closure(part.semantics)
            matches = [name for name, coordinate in coordinates.items() if coordinate.semantics.terms and self.entails(region, coordinate.semantics | coordinate.qualifiers)]
            if not matches:
                raise TypeError(f"{product}: no typed variable accepts {part.semantics}; include its role qualifiers")
            if len(matches) > 1:
                raise AmbiguousSemanticMatch(f"{part.semantics}: expected one variable region, matches {matches}")
            bindings[matches[0]].append(part)
        value = {}
        for name, coordinate in coordinates.items():
            matched = bindings[name]
            if not coordinate.many and len(matched) > 1:
                raise AmbiguousSemanticMatch(f"{product}: variable {coordinate.semantics} has multiple values")
            if matched:
                values = [SemanticValue(part.semantics, part.value, unit=part.unit) for part in matched]
                value[name] = values if coordinate.many else values[0]
            elif coordinate.many and not coordinate.optional:
                value[name] = []
            elif coordinate.has_default:
                value[name] = deepcopy(coordinate.default)
        self.validate_value(product, value, partial=partial)
        return SemanticValue(product, value, partial)

    def closure(self, product: Product) -> Product:
        return Product(self._closure(self.product(product).terms))

    def _assertion_terms(self, name: str) -> list[str]:
        return self.aliases.get(name, [name])

    def _closure(self, start: frozenset[str] | set[str]) -> frozenset[str]:
        terms = set(start)
        changed = True
        while changed:
            changed = False
            for rule in self.active_rules:
                if rule.kind not in ("implication", "requirement"):
                    continue
                if not rule.when.evaluate(terms):
                    continue
                for name in rule.then.forced_terms():
                    for term in self._assertion_terms(name):
                        if term not in terms:
                            terms.add(term)
                            changed = True
        return frozenset(terms)

    def consistent(self, terms: frozenset[str], depth: int = 0) -> bool:
        if depth > MAX_SOLVER_DEPTH:
            raise SemanticSolverLimit("semantic consistency depth exceeded")
        by_axis: dict[str, set[str]] = {}
        for term in terms:
            axis = self.axis_of_value.get(term)
            if axis:
                by_axis.setdefault(axis, set()).add(term)
        for axis, values in by_axis.items():
            if self.axis_cardinality.get(axis) == "one" and len(values) > 1:
                return False
        for rule in self.active_rules:
            if rule.kind == "disjointness":
                if rule.left.evaluate(terms) and rule.right.evaluate(terms):
                    return False
            elif rule.kind == "exclusion":
                if rule.when.evaluate(terms):
                    return False
        for rule in self.active_rules:
            if rule.kind not in ("implication", "requirement", "applicability"):
                continue
            if not rule.when.evaluate(terms):
                continue
            if rule.then.evaluate(terms):
                continue
            # A requirement may stay undecided in a partial product. It is
            # illegal only when no completion can satisfy it.
            if not self.satisfiable(rule.then, terms, depth + 1):
                return False
        return True

    def satisfiable(self, expr: Expr, terms: frozenset[str], depth: int = 0) -> bool:
        return bool(self._candidates(expr, terms, depth))

    def _candidates(
        self, expr: Expr, terms: frozenset[str], depth: int
    ) -> list[frozenset[str]]:
        if depth > MAX_SOLVER_DEPTH:
            raise SemanticSolverLimit("semantic candidate depth exceeded")
        if expr.evaluate(terms):
            return [terms]
        if isinstance(expr, Not):
            return [terms] if not expr.item.evaluate(terms) else []
        if isinstance(expr, Any):
            out: list[frozenset[str]] = []
            for item in expr.items:
                out.extend(self._candidates(item, terms, depth + 1))
            return _dedupe(out)
        if isinstance(expr, All):
            frontier: list[frozenset[str]] = [terms]
            for item in expr.items:
                nxt: list[frozenset[str]] = []
                for candidate in frontier:
                    nxt.extend(self._candidates(item, candidate, depth + 1))
                frontier = _dedupe(nxt)
                if len(frontier) > MAX_CANDIDATES:
                    raise SemanticSolverLimit("semantic candidate limit exceeded")
                if not frontier:
                    return []
            return frontier
        if isinstance(expr, Term):
            candidate = self._closure(terms | set(self._assertion_terms(expr.name)))
            return [candidate] if self.consistent(candidate, depth + 1) else []
        return []

    def legal(self, product: Product) -> bool:
        return self.consistent(self._closure(self.product(product).terms))

    def entails(self, product: Product, wanted: Any) -> bool:
        return self.closure(self.product(wanted)).terms <= self.closure(self.product(product)).terms

    def equivalent(self, left: Product, right: Product) -> bool:
        return self.closure(left) == self.closure(right)

    def applicable(self, product: Product, term: Any) -> bool:
        # Meaningfulness is emergent: a product gains a dimension when the
        # dimension's region can hold in it, even though the product does not
        # assert that dimension.
        axis_name = term.axis if isinstance(term, AxisValue) else str(term)
        region = self.axis_region.get(axis_name)
        closed = self.closure(product).terms
        if region is not None and not self.satisfiable(region, closed):
            return False
        for extra in self.term_applicability.get(axis_name, ()):
            if not self.satisfiable(extra, closed):
                return False
        return True


PRIMITIVE_TYPES = {"float": float, "int": int, "string": str, "bool": bool, "bytes": bytes}


def _dedupe(items: list[frozenset[str]]) -> list[frozenset[str]]:
    return list(dict.fromkeys(items))


def subject_identity(uid: Any) -> str | bytes:
    if isinstance(uid, str) and uid:
        return uid
    if isinstance(uid, bytes):
        return UID(uid)
    raise ValueError("subject identity requires nonempty text or a 16-byte UID")


class SubjectRef:
    def __init__(self, store: "Store", uid: str | bytes):
        self.store = store
        self.uid = subject_identity(uid)

    @property
    def semantics(self) -> Product:
        return self.store._subjects[self.uid]

    def assert_(self, *terms: Any) -> "SubjectRef":
        self.store.ref(self.uid, *terms)
        return self

    def set(self, semantics: Any, value: Any, **metadata: Any) -> Datum:
        return self.store.set(self, semantics, value, **metadata)

    def get(self, *query: Any) -> Datum:
        return self.store.get(self, *query)

    def find(self, *query: Any) -> list[Datum]:
        return self.store.find(self, *query)

    def __repr__(self) -> str:
        return f"Ref({self.uid!r}, {self.semantics})"


class OpenExpression:
    def __init__(self, store: "Store", ref: SubjectRef, expression: ExpressionType, definition_id: str):
        self.store = store
        self.ref = ref
        self.expression = expression
        self.definition_id = definition_id
        self.bindings = {}

    @property
    def factors(self) -> Product:
        return self.expression.factors

    def bind(self, name: str, value: SubjectRef | Datum | Component | SemanticValue, *, interpretation: str = "current") -> "OpenExpression":
        if name not in self.expression.variables:
            raise KeyError(f"{self.expression.name} has no variable {name!r}")
        registry = self.store.registry.at(self.definition_id)
        region = registry.closure(self.expression.variables[name])
        if isinstance(value, SubjectRef):
            if value.store is not self.store:
                raise ValueError(f"{name}: reference belongs to another store")
            if interpretation not in ("current", "recorded"):
                raise ValueError("interpretation must be current or recorded")
            meaning = value.semantics if interpretation == "recorded" else self.store.registry.closure(value.semantics)
        elif isinstance(value, Datum):
            meaning = self.store.meaning_of(value, interpretation=interpretation)
        elif isinstance(value, (Component, SemanticValue)):
            if interpretation not in ("current", "recorded"):
                raise ValueError("interpretation must be current or recorded")
            model = self.store.registry if interpretation == "current" else registry
            model.validate_value(value.semantics, value.value)
            meaning = model.closure(value.semantics)
        else:
            raise TypeError(f"{name}: not a semantic binding: {value!r}")
        if not region.terms <= meaning.terms:
            raise TypeError(f"{name}: {meaning} does not satisfy {region}")
        self.bindings = {**self.bindings, name: value}
        return self

    def components(self) -> list[Component]:
        """Project bound variables with semantic participant and input/answer roles."""
        registry = self.store.registry.at(self.definition_id)
        components = []
        for name, value in self.bindings.items():
            role = self.expression.roles.get(name, EMPTY)
            mode = sem("BindingMode.Answer" if name in self.expression.sought else "BindingMode.Input")
            qualifiers = role | mode
            if isinstance(value, SubjectRef):
                region = self.expression.variables[name] | qualifiers | sem("Reference")
                variable = Coord(name, "reference", semantics=self.expression.variables[name], qualifiers=qualifiers)
                components.append(Component(region, registry.closure(region), registry, value.uid,
                                            variable=variable, _path=(self.ref.uid, name)))
            else:
                datum = value if isinstance(value, Datum) else value._datum if isinstance(value, Component) else None
                components.append(registry.decompose(value.semantics, value.value, datum=datum, partial=True,
                                                     _qualifiers=qualifiers, _path=(self.ref.uid, name)))
        return components

    def find(self, *query: Any) -> list[Component]:
        registry = self.store.registry.at(self.definition_id)
        question = _question(registry, query)
        return question.select([part for component in self.components() for part in component.walk()
                                if question.semantics.terms <= part.meaning.terms and part.contains(question.contains) and question.accepts(part)])

    def get(self, *query: Any) -> Component:
        found = self.find(*query)
        if not found:
            raise KeyError(f"no bound variable satisfies {query!r}")
        if len(found) != 1:
            raise AmbiguousSemanticMatch(f"{query!r} matches {len(found)} bound components")
        return found[0]

    @property
    def unbound(self) -> list[str]:
        return [name for name in self.expression.variables if name not in self.bindings]

    def solve(self, **questions: Query) -> dict[str, Any]:
        unknown = questions.keys() - self.expression.sought.keys()
        if unknown:
            raise KeyError(f"{self.expression.name}: unknown sought variables {sorted(unknown)}")
        if any(not isinstance(question, Query) for question in questions.values()):
            raise TypeError("expression answer constraints require Query values")
        values = {}
        registry = self.store.registry.at(self.definition_id)
        for equation in self.expression.equations:
            if equation.equals not in self.expression.sought:
                continue
            region = registry.closure(registry.product(equation.quantity))
            question = _question(self.store.registry, (questions.get(equation.equals, Query()).narrow(region),))
            if equation.equals in self.bindings:
                if equation.equals in questions:
                    raise ValueError(f"{equation.equals}: cannot select evidence for an explicitly bound variable")
                values[equation.equals] = self.bindings[equation.equals]
                continue
            source = self.bindings.get(equation.of)
            if not isinstance(source, SubjectRef):
                continue
            value = self.store.value_of(source, question)
            if value is not None:
                values[equation.equals] = value
        return values

    def __str__(self) -> str:
        given = ", ".join(f"{name}={_render_binding(self.bindings.get(name))}" for name in self.expression.given)
        text = f"{self.expression.name}({given})"
        if self.expression.sought:
            text += " => " + ", ".join(f"{name}={_render_binding(self.bindings.get(name))}" for name in self.expression.sought)
        return text


def _render_binding(value: Any) -> str:
    if value is None:
        return "?"
    if isinstance(value, SubjectRef):
        return str(value.uid)
    return repr(value.value)


class Store:
    """In-memory subjects and facts addressed by their semantic meaning."""

    def __init__(self, registry: SemanticRegistry | None = None):
        self._subjects = {}
        self._data = {}
        self._facts = {}
        self._relations = []
        self._expressions = {}
        self.registry = registry if registry is not None else SemanticRegistry.load(Path(__file__).with_name("definitions.yaml"))

    def _add_fact(self, datum: Datum):
        self._data.setdefault(datum.subject, []).append(datum)
        self._facts[datum.id] = datum

    def ref(self, uid: str | bytes, *semantics: Any) -> SubjectRef:
        uid = subject_identity(uid)
        if uid in self._subjects and not semantics:
            return SubjectRef(self, uid)
        candidate = self._subjects.get(uid, EMPTY) | self.registry.product(*semantics)
        if not self.registry.legal(candidate):
            raise IllegalSemanticCombination(f"{uid}: incompatible subject semantics {candidate}")
        candidate = self.registry.closure(candidate)
        self._subjects[uid] = candidate
        return SubjectRef(self, uid)

    def _check_subject(self, subject: SubjectRef):
        if not isinstance(subject, SubjectRef) or subject.store is not self:
            raise ValueError("subject reference belongs to another store")

    def set(self, subject: SubjectRef, semantics: Any, value: Any, *, source: Any = None, observed_at: Any = None, validity: Any = None, provenance: dict | None = None, partial: bool = False, unit: str | None = None) -> Datum:
        self._check_subject(subject)
        product = self.registry.product(semantics)
        if not self.registry.legal(product):
            raise IllegalSemanticCombination(f"illegal datum semantics: {product}")
        if isinstance(value, SemanticValue):
            if not self.registry.entails(value.semantics, product):
                raise TypeError(f"{value.semantics} does not satisfy {product}")
            product |= self.registry.product(value.semantics)
            partial = partial or value.partial
            if unit is not None and value.unit is not None and unit != value.unit:
                raise ValueError("explicit unit differs from semantic value unit")
            unit = value.unit if value.unit is not None else unit
            value = value.value
        if type(partial) is not bool or (unit is not None and not isinstance(unit, str)):
            raise TypeError("partial must be boolean and unit must be text")
        self.registry.validate_value(product, value, partial=partial)
        if provenance is not None and not isinstance(provenance, dict):
            raise TypeError("datum provenance must be a mapping")
        datum = Datum(str(uuid4()), subject.uid, product, self.registry.closure(product), self.registry.definition_id, value, self.registry._revision, source, observed_at, validity, provenance or {}, partial=partial, unit=unit)
        self._add_fact(datum)
        return datum

    def add(self, datum: Datum) -> Datum:
        """Import an observation without reinterpreting it under local definitions."""
        if not isinstance(datum, Datum):
            raise TypeError("add requires a semantic datum")
        if not isinstance(datum.id, str) or not datum.id:
            raise ValueError("fact identity must be nonempty text")
        subject_identity(datum.subject)
        if datum.definition_id != datum._definitions.id:
            raise ValueError("fact definition identity does not match its definitions")
        registry = self.registry.at(datum.definition_id) if datum.definition_id in self.registry._history else SemanticRegistry(datum.definitions)
        if not registry.legal(datum.semantics) or registry.closure(datum.semantics) != datum.meaning:
            raise ValueError("fact meaning does not match its original definitions")
        registry.validate_value(datum.semantics, datum.value, partial=datum.partial)
        if not isinstance(datum.provenance, dict):
            raise ValueError("fact provenance must be a mapping")
        existing = self._facts.get(datum.id)
        if existing is not None:
            if existing != datum:
                raise ValueError(f"fact {datum.id}: identity already has different data")
            return existing
        new_subject = datum.subject not in self._subjects
        if new_subject:
            self._subjects[datum.subject] = EMPTY
        self.registry._history[datum.definition_id] = datum._definitions
        self._add_fact(datum)
        return datum

    def find(self, subject: SubjectRef, *query: Any) -> list[Datum]:
        self._check_subject(subject)
        question = _question(self.registry, query)
        found = []
        for datum in self._data.get(subject.uid, []):
            meaning = datum.meaning if question.interpretation == "recorded" else self.registry.closure(datum.semantics)
            if question.semantics.terms <= meaning.terms:
                if not question.accepts(datum):
                    continue
                if question.contains:
                    registry = self.registry.at(datum.definition_id) if question.interpretation == "recorded" else self.registry
                    if not registry.decompose(datum.semantics, datum.value, datum=datum, partial=True, _unit=datum.unit).contains(question.contains):
                        continue
                self.meaning_of(datum, interpretation=question.interpretation)
                found.append(datum)
                continue
            registry = self.registry.at(datum.definition_id) if question.interpretation == "recorded" else self.registry
            # Current charts are interpretations of retained evidence. A newly
            # declared required variable may still be unknown in older data.
            composition = registry.decompose(datum.semantics, datum.value, datum=datum, partial=True, _unit=datum.unit)
            matches = composition.find(question)
            if matches:
                self.meaning_of(datum, interpretation=question.interpretation)
                found.extend(matches)
        if question.semantics.terms and subject.uid in self._expressions:
            found.extend(self._expressions[subject.uid].find(question))
        return question.select(found)

    def meaning_of(self, datum: Datum, *, interpretation: str = "current") -> Product:
        """Evaluate an observation without replacing its recorded meaning or value."""
        if interpretation == "recorded":
            return datum.meaning
        if interpretation != "current":
            raise ValueError("interpretation must be current or recorded")
        if not self.registry.legal(datum.semantics):
            raise IllegalSemanticCombination(f"fact {datum.id}: current model contradicts recorded semantics {datum.semantics}; recorded meaning remains available")
        return self.registry.closure(datum.semantics)

    def get(self, subject: SubjectRef, *query: Any) -> Datum:
        found = self.find(subject, *query)
        region = _question(self.registry, query).semantics
        if not found:
            raise KeyError(f"no semantic match for {subject.uid}: {region}")
        if len(found) > 1:
            raise AmbiguousSemanticMatch(f"{subject.uid}: {region} matches fact IDs {[datum.id for datum in found]}")
        return found[0]

    def get_many(self, subjects: Iterable[SubjectRef], *query: Any) -> dict[str | bytes, Datum]:
        return {subject.uid: self.get(subject, *query) for subject in subjects}

    def value_of(self, subject: SubjectRef, region: Product | Query) -> Datum | SubjectRef | None:
        self._check_subject(subject)
        question = _question(self.registry, (region,))
        subject_meaning = subject.semantics if question.interpretation == "recorded" else self.registry.closure(subject.semantics)
        found = ([subject] if not question.constrained_evidence and question.semantics.terms <= subject_meaning.terms else []) + self.find(subject, question)
        if len(found) > 1:
            raise AmbiguousSemanticMatch(f"{subject.uid}: {question.semantics} matches {len(found)} independent facts")
        return found[0] if found else None

    def task(self, uid: str | bytes, word: str, **value: Any) -> OpenExpression:
        uid = subject_identity(uid)
        if uid in self._expressions:
            raise ValueError(f"expression {uid} already exists")
        expression_type = self.registry.expression_of(word)
        variable = "intent" if word.startswith("TaskIntent.") else "operation" if word.startswith("CommandOperation.") else "word"
        data = {**value, "uid": uid, variable: word}
        self.registry.validate_value(expression_type.factors, data, partial=True)
        ref = self.ref(uid, expression_type.factors)
        self.set(ref, expression_type.factors, data, provenance={"kind": "expression"}, partial=True)
        expression = OpenExpression(self, ref, expression_type, self.registry.definition_id)
        self._expressions[uid] = expression
        return expression

    def expression(self, uid: str | bytes) -> OpenExpression:
        return self._expressions[subject_identity(uid)]

    def relate(self, relation: str | RelationType, *operands: SubjectRef, **roles: SubjectRef) -> RelationFact:
        relation = self.registry.relation_types[relation] if isinstance(relation, str) else relation
        if relation.definition_id not in self.registry._history:
            raise ValueError("relation definition does not belong to this store")
        fact = relation(*operands, **roles)
        if any(isinstance(operand, SubjectRef) and operand.store is not self for operand in fact.operands):
            raise ValueError("relation operands belong to another store")
        self._relations.append(fact)
        return fact

    def relations(self, relation: str | RelationType | None = None) -> list[RelationFact]:
        if relation is None:
            return list(self._relations)
        relation = self.registry.relation_types[relation] if isinstance(relation, str) else relation
        return [fact for fact in self._relations if fact.relation.is_a(relation)]

    def interpret(self, original: Datum, mapping_name: str) -> Datum:
        if original.id not in self._facts:
            raise ValueError("source datum does not belong to this store")
        if self._facts[original.id] != original:
            raise ValueError(f"source datum {original.id} differs from its stored observation")
        mapping = self.registry.mappings[mapping_name]
        raw = original.value
        fields = mapping.get("fields", {})
        if fields:
            if not isinstance(raw, dict):
                raise TypeError(f"mapping {mapping_name}: expected source field mapping")
            value = {target: raw[source] for target, source in fields.items()}
        else:
            value = raw
        return self.set(SubjectRef(self, original.subject), product_names(mapping["semantics"]), value, source=original.source, observed_at=original.observed_at, validity=original.validity, provenance={"kind": "mapped", "mapping": mapping_name, "derived_from": [original.id], "context": deepcopy(mapping.get("context", {}))})


def value_semantics(value: Datum | SubjectRef | Component | SemanticValue) -> Product:
    if isinstance(value, Component):
        return value.meaning
    if isinstance(value, SemanticValue):
        return value.semantics
    if isinstance(value, Datum):
        return value.meaning
    if isinstance(value, SubjectRef):
        return value.semantics
    raise TypeError(f"not a semantic value: {value!r}")
