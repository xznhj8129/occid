from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from hashlib import sha256
from math import isfinite
from pathlib import Path
import sqlite3
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
    type: str
    unit: str | None = None
    optional: bool = False

    def __str__(self) -> str:
        return f"{self.name}:{self.type}" + (f"[{self.unit}]" if self.unit else "")


@dataclass(frozen=True, slots=True)
class ChartType:
    display: str
    factors: Product
    coords: tuple[Coord, ...]
    _context: dict = field(default_factory=dict, repr=False)

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

    def __post_init__(self):
        object.__setattr__(self, "given", MappingProxyType(dict(self.given)))
        object.__setattr__(self, "sought", MappingProxyType(dict(self.sought)))

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


@dataclass(frozen=True)
class Datum:
    """One immutable observation, with its original definition revision."""
    id: str
    subject: str | bytes
    semantics: Product
    meaning: Product
    definition_id: str
    _value: Any = field(repr=False)
    _definitions: dict = field(repr=False)
    _source: Any = field(default=None, repr=False)
    _observed_at: Any = field(default=None, repr=False)
    _validity: Any = field(default=None, repr=False)
    _provenance: dict = field(default_factory=dict, repr=False)
    _extensions: dict = field(default_factory=dict, repr=False)

    def __post_init__(self):
        for name in ("_value", "_definitions", "_source", "_observed_at", "_validity", "_provenance", "_extensions"):
            object.__setattr__(self, name, deepcopy(getattr(self, name)))

    @property
    def value(self):
        return deepcopy(self._value)

    @property
    def definitions(self):
        return deepcopy(self._definitions)

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

    def encode(self) -> bytes:
        from .wire import encode
        return encode(self)


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
            if not isinstance(operand, SubjectRef) or not expected.terms <= operand.semantics.terms:
                raise TypeError(f"{self.name} operand {role!r} expects {expected}, got {operand!r}")
        if any(operand.store is not operands[0].store for operand in operands):
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
        parts = (f"{role}={operand.uid}" for role, operand in zip(self.relation.operand_names, self.operands))
        return f"{self.relation.name}({', '.join(parts)})"


def definition_identity(spec: dict) -> str:
    # Map order matters for relation operand order; do not sort it away.
    return sha256(msgpack.packb(spec, use_bin_type=True)).hexdigest()


class SemanticRegistry:
    def __init__(self, spec: dict[str, Any]):
        self._spec = deepcopy(spec)
        data = prepare(spec)
        self.definition_id = definition_identity(self._spec)
        self._history = {self.definition_id: self._spec}
        self._persist = None
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
                tuple(Coord(coord["name"], coord["type"], coord["unit"], bool(coord["optional"])) for coord in item["coords"]),
                item["context"],
            )
            for item in data["charts"]
        ]
        self.expressions = {name: ExpressionType(name, product_names(item["factors"]), {role: product_names(region) for role, region in item["given"].items()}, {role: product_names(region) for role, region in item["sought"].items()}, tuple(Equation(**equation) for equation in item["equations"]), tuple(item["words"])) for name, item in data["expressions"].items()}
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
        if not isinstance(changes, dict) or changes.keys() - set(SECTIONS):
            raise ValueError(f"definition updates must name sections {SECTIONS}")
        revised = self.spec
        for section, entries in changes.items():
            if not isinstance(entries, dict):
                raise ValueError(f"definition update {section}: expected mapping")
            revised.setdefault(section, {}).update(deepcopy(entries))
        candidate = SemanticRegistry(revised)
        if self._persist is not None:
            self._persist(candidate)
        history = {**self._history, candidate.definition_id: candidate._spec}
        persist = self._persist
        self.__dict__.update(candidate.__dict__)
        self._history = history
        self._persist = persist

    def at(self, definition_id: str) -> "SemanticRegistry":
        return SemanticRegistry(self._history[definition_id])

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

    def validate_value(self, product: Product, value: Any) -> None:
        coordinates = self.coordinates(product)
        if not coordinates:
            return
        if not isinstance(value, dict):
            raise TypeError(f"{product}: chart value must be a mapping")
        for name, coordinate in coordinates.items():
            if name not in value:
                if coordinate.optional:
                    continue
                raise ValueError(f"{product}: missing coordinate {name!r}")
            item = value[name]
            if item is None and coordinate.optional:
                continue
            expected = PRIMITIVE_TYPES[coordinate.type]
            if coordinate.type == "float":
                valid = type(item) in (int, float) and isfinite(item)
            else:
                valid = type(item) is expected
            if not valid:
                raise TypeError(f"{product}: {name}={item!r} requires {coordinate}")

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

    def bind(self, name: str, value: SubjectRef | Datum) -> "OpenExpression":
        if name not in self.expression.variables:
            raise KeyError(f"{self.expression.name} has no variable {name!r}")
        registry = self.store.registry.at(self.definition_id)
        region = registry.closure(self.expression.variables[name])
        if isinstance(value, SubjectRef):
            if value.store is not self.store:
                raise ValueError(f"{name}: reference belongs to another store")
            meaning = value.semantics
        elif isinstance(value, Datum):
            meaning = value.meaning
        else:
            raise TypeError(f"{name}: not a semantic binding: {value!r}")
        if not region.terms <= meaning.terms:
            raise TypeError(f"{name}: {meaning} does not satisfy {region}")
        bindings = {**self.bindings, name: value}
        self.store._save_expression(self, bindings)
        self.bindings = bindings
        return self

    @property
    def unbound(self) -> list[str]:
        return [name for name in self.expression.variables if name not in self.bindings]

    def solve(self) -> dict[str, Any]:
        values = {}
        registry = self.store.registry.at(self.definition_id)
        for equation in self.expression.equations:
            if equation.equals not in self.expression.sought:
                continue
            if equation.equals in self.bindings:
                values[equation.equals] = self.bindings[equation.equals]
                continue
            source = self.bindings.get(equation.of)
            if not isinstance(source, SubjectRef):
                continue
            value = self.store.value_of(source, registry.closure(registry.product(equation.quantity)))
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
    def __init__(self, registry: SemanticRegistry | None = None, path: str | Path | None = None):
        self._closed = False
        self._db = sqlite3.connect(path) if path is not None else None
        self._subjects = {}
        self._data = {}
        self._facts = {}
        self._relations = []
        self._expressions = {}
        if self._db is not None:
            with self._db:
                self._db.execute("CREATE TABLE IF NOT EXISTS definitions (id TEXT PRIMARY KEY, payload BLOB NOT NULL)")
                self._db.execute("CREATE TABLE IF NOT EXISTS current_definition (singleton INTEGER PRIMARY KEY CHECK(singleton=1), id TEXT NOT NULL)")
                self._db.execute("CREATE TABLE IF NOT EXISTS subjects (uid BLOB PRIMARY KEY, payload BLOB NOT NULL)")
                self._db.execute("CREATE TABLE IF NOT EXISTS facts (id TEXT PRIMARY KEY, payload BLOB NOT NULL)")
                self._db.execute("CREATE TABLE IF NOT EXISTS relations (id TEXT PRIMARY KEY, payload BLOB NOT NULL)")
                self._db.execute("CREATE TABLE IF NOT EXISTS expressions (uid BLOB PRIMARY KEY, payload BLOB NOT NULL)")
            active = self._db.execute("SELECT id FROM current_definition WHERE singleton=1").fetchone()
            if active:
                definitions = {identity: _unpack(payload) for identity, payload in self._db.execute("SELECT id, payload FROM definitions")}
                stored = SemanticRegistry(definitions[active[0]])
                if registry is not None and registry.definition_id != stored.definition_id:
                    self._db.close()
                    raise ValueError("persistent store already has different definitions; open it without a registry, then update")
                registry = stored
                registry._history = definitions
        self.registry = registry if registry is not None else SemanticRegistry.load(Path(__file__).with_name("definitions.yaml"))
        if self.registry._persist is not None:
            raise ValueError("registry already belongs to a persistent store")
        if self._db is not None:
            self._save_definitions(self.registry)
            self.registry._persist = self._save_definitions
            self._reload()

    def _save_definitions(self, candidate: SemanticRegistry):
        with self._db:
            for identity, spec in candidate._history.items():
                self._db.execute("INSERT OR IGNORE INTO definitions VALUES (?, ?)", (identity, _pack(spec)))
            self._db.execute("INSERT INTO current_definition VALUES (1, ?) ON CONFLICT(singleton) DO UPDATE SET id=excluded.id", (candidate.definition_id,))

    def _reload(self):
        from .wire import decode
        for uid, payload in self._db.execute("SELECT uid, payload FROM subjects"):
            self._subjects[uid] = product_names(_unpack(payload))
        for _, payload in self._db.execute("SELECT id, payload FROM facts ORDER BY rowid"):
            self._add_fact(decode(payload))
        for _, payload in self._db.execute("SELECT id, payload FROM relations ORDER BY rowid"):
            item = _unpack(payload)
            registry = self.registry.at(item["definition_id"])
            self._relations.append(RelationFact(item["id"], registry.relation_types[item["name"]], tuple(SubjectRef(self, uid) for uid in item["operands"])))
        for uid, payload in self._db.execute("SELECT uid, payload FROM expressions"):
            item = _unpack(payload)
            registry = self.registry.at(item["definition_id"])
            expression = OpenExpression(self, SubjectRef(self, uid), registry.expressions[item["name"]], registry.definition_id)
            for name, binding in item["bindings"].items():
                kind = binding["kind"]
                if kind == "subject":
                    value = SubjectRef(self, binding["id"])
                elif kind == "fact":
                    value = self._facts[binding["id"]]
                elif kind == "datum":
                    value = decode(binding["payload"])
                else:
                    raise ValueError(f"expression {uid}: unknown persisted binding kind {kind!r}")
                expression.bindings[name] = value
            self._expressions[uid] = expression

    def _add_fact(self, datum: Datum):
        self._data.setdefault(datum.subject, []).append(datum)
        self._facts[datum.id] = datum

    def ref(self, uid: str | bytes, *semantics: Any) -> SubjectRef:
        self._ensure_open()
        uid = subject_identity(uid)
        if uid in self._subjects and not semantics:
            return SubjectRef(self, uid)
        candidate = self._subjects.get(uid, EMPTY) | self.registry.product(*semantics)
        if not self.registry.legal(candidate):
            raise IllegalSemanticCombination(f"{uid}: incompatible subject semantics {candidate}")
        candidate = self.registry.closure(candidate)
        if self._db is not None:
            with self._db:
                self._db.execute("INSERT INTO subjects VALUES (?, ?) ON CONFLICT(uid) DO UPDATE SET payload=excluded.payload", (uid, _pack(list(candidate))))
        self._subjects[uid] = candidate
        return SubjectRef(self, uid)

    def _check_subject(self, subject: SubjectRef):
        self._ensure_open()
        if not isinstance(subject, SubjectRef) or subject.store is not self:
            raise ValueError("subject reference belongs to another store")

    def _ensure_open(self):
        if self._closed:
            raise RuntimeError("store is closed")

    def set(self, subject: SubjectRef, semantics: Any, value: Any, *, source: Any = None, observed_at: Any = None, validity: Any = None, provenance: dict | None = None) -> Datum:
        self._check_subject(subject)
        product = self.registry.product(semantics)
        if not self.registry.legal(product):
            raise IllegalSemanticCombination(f"illegal datum semantics: {product}")
        self.registry.validate_value(product, value)
        if provenance is not None and not isinstance(provenance, dict):
            raise TypeError("datum provenance must be a mapping")
        datum = Datum(str(uuid4()), subject.uid, product, self.registry.closure(product), self.registry.definition_id, value, self.registry.spec, source, observed_at, validity, provenance or {})
        return self.add(datum)

    def add(self, datum: Datum) -> Datum:
        """Import an observation without reinterpreting it under local definitions."""
        from .wire import decode
        self._ensure_open()
        payload = datum.encode()
        datum = decode(payload)
        existing = self._facts.get(datum.id)
        if existing is not None:
            if existing != datum:
                raise ValueError(f"fact {datum.id}: identity already has different data")
            return existing
        new_subject = datum.subject not in self._subjects
        if self._db is not None:
            with self._db:
                self._db.execute("INSERT OR IGNORE INTO definitions VALUES (?, ?)", (datum.definition_id, _pack(datum.definitions)))
                if new_subject:
                    self._db.execute("INSERT INTO subjects VALUES (?, ?)", (datum.subject, _pack([])))
                self._db.execute("INSERT INTO facts VALUES (?, ?)", (datum.id, payload))
        if new_subject:
            self._subjects[datum.subject] = EMPTY
        self.registry._history[datum.definition_id] = datum.definitions
        self._add_fact(datum)
        return datum

    def find(self, subject: SubjectRef, *query: Any) -> list[Datum]:
        self._check_subject(subject)
        wanted = self.registry.product(*query)
        if not self.registry.legal(wanted):
            raise IllegalSemanticCombination(f"illegal semantic query: {wanted}")
        # Assertions already carry their historical closure. A new mapping or
        # implication never changes the original fact's meaning.
        return [datum for datum in self._data.get(subject.uid, []) if wanted.terms <= datum.meaning.terms]

    def get(self, subject: SubjectRef, *query: Any) -> Datum:
        found = self.find(subject, *query)
        if not found:
            raise KeyError(f"no semantic match for {subject.uid}: {sem(*query)}")
        if len(found) > 1:
            raise AmbiguousSemanticMatch(f"{subject.uid}: {sem(*query)} matches fact IDs {[datum.id for datum in found]}")
        return found[0]

    def get_many(self, subjects: Iterable[SubjectRef], *query: Any) -> dict[str | bytes, Datum]:
        return {subject.uid: self.get(subject, *query) for subject in subjects}

    def value_of(self, subject: SubjectRef, region: Product) -> Datum | SubjectRef | None:
        self._check_subject(subject)
        found = ([subject] if region.terms <= subject.semantics.terms else []) + [datum for datum in self._data.get(subject.uid, []) if region.terms <= datum.meaning.terms]
        if len(found) > 1:
            raise AmbiguousSemanticMatch(f"{subject.uid}: {region} matches {len(found)} independent facts")
        return found[0] if found else None

    def task(self, uid: str | bytes, word: str, **value: Any) -> OpenExpression:
        self._ensure_open()
        uid = subject_identity(uid)
        if uid in self._expressions:
            raise ValueError(f"expression {uid} already exists")
        expression_type = self.registry.expression_of(word)
        ref = self.ref(uid, expression_type.factors)
        self.set(ref, expression_type.factors, {**value, "word": word}, provenance={"kind": "expression"})
        expression = OpenExpression(self, ref, expression_type, self.registry.definition_id)
        self._save_expression(expression, {})
        self._expressions[uid] = expression
        return expression

    def _save_expression(self, expression: OpenExpression, bindings: dict):
        self._ensure_open()
        if self._db is None:
            return
        recorded = {}
        for name, value in bindings.items():
            if isinstance(value, SubjectRef):
                recorded[name] = {"kind": "subject", "id": value.uid}
            elif value.id in self._facts:
                recorded[name] = {"kind": "fact", "id": value.id}
            else:
                recorded[name] = {"kind": "datum", "payload": value.encode()}
        item = {"name": expression.expression.name, "definition_id": expression.definition_id, "bindings": recorded}
        with self._db:
            self._db.execute("INSERT INTO expressions VALUES (?, ?) ON CONFLICT(uid) DO UPDATE SET payload=excluded.payload", (expression.ref.uid, _pack(item)))

    def expression(self, uid: str | bytes) -> OpenExpression:
        self._ensure_open()
        return self._expressions[subject_identity(uid)]

    def relate(self, relation: str | RelationType, *operands: SubjectRef, **roles: SubjectRef) -> RelationFact:
        self._ensure_open()
        relation = self.registry.relation_types[relation] if isinstance(relation, str) else relation
        if relation.definition_id not in self.registry._history:
            raise ValueError("relation definition does not belong to this store")
        fact = relation(*operands, **roles)
        if fact.operands[0].store is not self:
            raise ValueError("relation operands belong to another store")
        if self._db is not None:
            item = {"id": fact.id, "name": relation.name, "definition_id": relation.definition_id, "operands": [operand.uid for operand in fact.operands]}
            with self._db:
                self._db.execute("INSERT INTO relations VALUES (?, ?)", (fact.id, _pack(item)))
        self._relations.append(fact)
        return fact

    def relations(self, relation: str | RelationType | None = None) -> list[RelationFact]:
        self._ensure_open()
        if relation is None:
            return list(self._relations)
        relation = self.registry.relation_types[relation] if isinstance(relation, str) else relation
        return [fact for fact in self._relations if fact.relation.is_a(relation)]

    def interpret(self, original: Datum, mapping_name: str) -> Datum:
        self._ensure_open()
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

    def close(self):
        if self._db is not None:
            self.registry._persist = None
            self._db.close()
            self._db = None
        self._closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()


def _pack(value: Any) -> bytes:
    return msgpack.packb(value, use_bin_type=True)


def _unpack(payload: bytes) -> Any:
    return msgpack.unpackb(payload, raw=False, strict_map_key=False)


def value_semantics(value: Datum | SubjectRef) -> Product:
    if isinstance(value, Datum):
        return value.meaning
    if isinstance(value, SubjectRef):
        return value.semantics
    raise TypeError(f"not a semantic value: {value!r}")
